from __future__ import annotations

from pathlib import Path

from pydub import AudioSegment

from app.core.logger import get_logger
from app.core.timeline import Timeline
import time

TIMELINE_PATH = Path("data/output/timeline.json")
AUDIO_PATH = Path("data/output/audio/narration.wav")

logger = get_logger("stage3_voice")


def _scene_duration_seconds(scene: dict) -> float:
    return float(scene.get("duration_seconds") or scene.get("duration") or 6.0)


def run() -> None:
    logger.info("Starting Stage 3 placeholder voice generation")
    started_at = time.perf_counter()

    timeline = Timeline.load(TIMELINE_PATH)
    AUDIO_PATH.parent.mkdir(parents=True, exist_ok=True)

    total_ms = int(
        sum(_scene_duration_seconds(scene) for scene in timeline.scenes) * 1000
    )

    silent = AudioSegment.silent(duration=total_ms)
    silent.export(AUDIO_PATH, format="wav")

    timeline.data.setdefault("assets", {})
    timeline.data["assets"]["narration_audio"] = str(AUDIO_PATH)

    for scene in timeline.scenes:
        scene["audio_path"] = str(AUDIO_PATH)
        scene.setdefault("status", {})["voice"] = "done"

    timeline.save(TIMELINE_PATH)

    elapsed = time.perf_counter() - started_at
    logger.info(
        "Stage 3 complete: created placeholder narration path=%s duration_ms=%s elapsed=%.2fs",
        AUDIO_PATH,
        total_ms,
        elapsed,
    )


if __name__ == "__main__":
    run()
