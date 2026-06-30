from __future__ import annotations

import os
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.core.timeline import Timeline
from app.images import ImageGenerationRequest, create_image_provider
from app.images.cache import ImageCache
import time

TIMELINE_PATH = Path("data/output/timeline.json")

logger = get_logger("stage2_images")


def _parse_resolution(resolution: str) -> tuple[int, int]:
    width_text, height_text = resolution.lower().split("x", maxsplit=1)
    return int(width_text), int(height_text)


def _get_scene_id(scene: dict) -> str:
    return str(scene.get("scene_id") or scene.get("id"))


def _get_force_enabled() -> bool:
    return os.getenv("FORCE", "0") == "1"


def _get_image_size() -> tuple[int, int]:
    configured_width = getattr(settings.images, "width", None)
    configured_height = getattr(settings.images, "height", None)

    if configured_width and configured_height:
        return int(configured_width), int(configured_height)

    return _parse_resolution(settings.render.resolution)


def _build_prompt(scene: dict) -> str:
    prompt = scene.get("image_prompt", "")
    style = getattr(settings.images, "style", "")

    if style:
        return f"{prompt}, {style}"

    return prompt


def _cache_extra() -> dict:
    return {
        "style": settings.images.style,
        "model_name": settings.images.model_name,
        "model_path": settings.images.model_path,
        "steps": settings.images.steps,
        "guidance_scale": settings.images.guidance_scale,
        "dtype": settings.images.dtype,
        "device": settings.images.device,
    }


def run() -> None:
    logger.info("Starting Stage 2 image generation")
    started_at = time.perf_counter()
    timeline = Timeline.load(TIMELINE_PATH)
    provider = create_image_provider(settings.images.provider)

    width, height = _get_image_size()
    force = _get_force_enabled()

    logger.info(
        "Using image provider=%s resolution=%sx%s cache_enabled=%s force=%s",
        provider.provider_name,
        width,
        height,
        settings.images.cache_enabled,
        force,
    )

    output_dir = Path("data/output/images")
    output_dir.mkdir(parents=True, exist_ok=True)

    cache_enabled = bool(getattr(settings.images, "cache_enabled", True))
    image_cache = ImageCache(Path("data/cache"))

    for scene in timeline.scenes:
        scene_id = _get_scene_id(scene)
        output_path = output_dir / f"{scene_id}.png"

        request = ImageGenerationRequest(
            scene_id=scene_id,
            prompt=_build_prompt(scene),
            negative_prompt=scene.get("negative_prompt", ""),
            output_path=output_path,
            width=width,
            height=height,
            seed=getattr(settings.images, "seed", None),
            force=force,
        )

        cache_key = image_cache.build_key(
            request=request,
            provider=provider.provider_name,
            extra=_cache_extra(),
        )

        try:
            if cache_enabled and not force and image_cache.has(cache_key):
                logger.info("Cache hit for %s", scene_id)
                result = image_cache.restore(
                    cache_key=cache_key,
                    request=request,
                    provider=provider.provider_name,
                )
            else:
                logger.info("Cache miss for %s; generating image", scene_id)
                result = provider.generate(request)

                if cache_enabled:
                    logger.info("Saving image cache for %s", scene_id)
                    image_cache.save(
                        cache_key=cache_key,
                        request=request,
                        result=result,
                        metadata={
                            "provider": provider.provider_name,
                            **_cache_extra(),
                            **result.metadata,
                        },
                    )

            scene["image_path"] = str(result.image_path)
            scene.setdefault("status", {})["image"] = (
                "skipped" if result.cached else "done"
            )
            scene.setdefault("image_metadata", {})
            scene["image_metadata"].update(
                {
                    "provider": result.provider,
                    "cached": result.cached,
                    "cache_key": cache_key,
                    "seed": result.seed,
                    "width": width,
                    "height": height,
                    **_cache_extra(),
                    **result.metadata,
                }
            )

            logger.info(
                "Completed image for %s path=%s cached=%s",
                scene_id,
                result.image_path,
                result.cached,
            )

        except Exception as exc:
            logger.exception("Image generation failed for %s", scene_id)

            scene.setdefault("status", {})["image"] = "failed"
            scene.setdefault("errors", [])
            scene["errors"].append(
                {
                    "stage": "stage2_images",
                    "message": str(exc),
                }
            )
            raise

    timeline.save(TIMELINE_PATH)
    elapsed = time.perf_counter() - started_at
    logger.info("Stage 2 complete: saved timeline=%s elapsed=%.2fs", TIMELINE_PATH, elapsed)


if __name__ == "__main__":
    run()
