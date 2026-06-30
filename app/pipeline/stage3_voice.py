from __future__ import annotations

import os
import time
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.core.timeline import Timeline
from app.voice import VoiceGenerationRequest, create_voice_provider
from app.voice.cache import VoiceCache

TIMELINE_PATH = Path("data/output/timeline.json")

logger = get_logger("stage3_voice")


def _get_scene_id(scene: dict) -> str:
    return str(scene.get("scene_id") or scene.get("id"))


def _scene_duration_seconds(scene: dict) -> float:
    return float(scene.get("duration_seconds") or scene.get("duration") or 6.0)


def _get_force_enabled() -> bool:
    return os.getenv("FORCE", "0") == "1"


def _cache_extra() -> dict:
    return {
        "voice_provider": settings.audio.voice_provider,
        "narration_volume": settings.audio.narration_volume,
    }


def run() -> None:
    logger.info("Starting Stage 3 voice generation")
    started_at = time.perf_counter()

    timeline = Timeline.load(TIMELINE_PATH)
    provider = create_voice_provider(
        settings.audio.voice_provider,
        settings.audio,
        )
    
    force = _get_force_enabled()

    output_dir = Path("data/output/audio")
    output_dir.mkdir(parents=True, exist_ok=True)

    sample_rate = int(getattr(settings.audio, "sample_rate", 24000))
    voice_name = str(getattr(settings.audio, "voice_name", "default"))
    cache_enabled = bool(getattr(settings.audio, "cache_enabled", True))
    voice_cache = VoiceCache(Path("data/cache"))

    logger.info(
        "Using voice provider=%s sample_rate=%s voice_name=%s cache_enabled=%s force=%s",
        provider.provider_name,
        sample_rate,
        voice_name,
        cache_enabled,
        force,
    )

    audio_assets: list[str] = []

    for scene in timeline.scenes:
        scene_id = _get_scene_id(scene)
        output_path = output_dir / f"{scene_id}.wav"

        request = VoiceGenerationRequest(
            scene_id=scene_id,
            text=str(scene.get("narration", "")),
            output_path=output_path,
            duration_seconds=_scene_duration_seconds(scene),
            sample_rate=sample_rate,
            voice_name=voice_name,
            force=force,
        )

        cache_key = voice_cache.build_key(
            request=request,
            provider=provider.provider_name,
            extra=_cache_extra(),
        )

        try:
            if cache_enabled and not force and voice_cache.has(cache_key):
                logger.info("Voice cache hit for %s", scene_id)
                result = voice_cache.restore(
                    cache_key=cache_key,
                    request=request,
                    provider=provider.provider_name,
                )
            else:
                logger.info("Voice cache miss for %s; generating audio", scene_id)
                result = provider.generate(request)

                if cache_enabled:
                    logger.info("Saving voice cache for %s", scene_id)
                    voice_cache.save(
                        cache_key=cache_key,
                        request=request,
                        result=result,
                        metadata={
                            "provider": provider.provider_name,
                            **_cache_extra(),
                            **result.metadata,
                        },
                    )

            scene["audio_path"] = str(result.audio_path)
            scene.setdefault("status", {})["voice"] = (
                "skipped" if result.cached else "done"
            )
            scene.setdefault("voice_metadata", {})
            scene["voice_metadata"].update(
                {
                    "provider": result.provider,
                    "cached": result.cached,
                    "cache_key": cache_key,
                    "duration_seconds": result.duration_seconds,
                    "sample_rate": sample_rate,
                    "voice_name": voice_name,
                    **_cache_extra(),
                    **result.metadata,
                }
            )

            audio_assets.append(str(result.audio_path))

            logger.info(
                "Completed voice for %s path=%s cached=%s duration=%.2fs",
                scene_id,
                result.audio_path,
                result.cached,
                result.duration_seconds,
            )

        except Exception as exc:
            logger.exception("Voice generation failed for %s", scene_id)
            scene.setdefault("status", {})["voice"] = "failed"
            scene.setdefault("errors", [])
            scene["errors"].append(
                {
                    "stage": "stage3_voice",
                    "message": str(exc),
                }
            )
            raise

    timeline.data.setdefault("assets", {})
    timeline.data["assets"]["scene_audio"] = audio_assets

    timeline.save(TIMELINE_PATH)

    elapsed = time.perf_counter() - started_at
    logger.info("Stage 3 complete: saved timeline=%s elapsed=%.2fs", TIMELINE_PATH, elapsed)


if __name__ == "__main__":
    run()
