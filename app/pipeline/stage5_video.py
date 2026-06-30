from __future__ import annotations

import time
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.core.timeline import Timeline
from app.renderer import RenderRequest, create_video_renderer

TIMELINE_PATH = Path("data/output/timeline.json")
SUBTITLE_PATH = Path("data/output/subtitles/subtitles.srt")
VIDEO_PATH = Path("data/output/videos/demo.mp4")

logger = get_logger("stage5_video")


def run() -> None:
    logger.info("Starting Stage 5 video render")
    started_at = time.perf_counter()

    timeline = Timeline.load(TIMELINE_PATH)
    renderer = create_video_renderer("ffmpeg")

    request = RenderRequest(
        timeline_data=timeline.data,
        output_path=VIDEO_PATH,
        subtitle_path=SUBTITLE_PATH,
        resolution=settings.render.resolution,
        fps=settings.render.fps,
        codec=settings.render.codec,
        crf=settings.render.crf,
        preset=settings.render.preset,
    )

    result = renderer.render(request)

    for scene in timeline.scenes:
        scene.setdefault("status", {})["render"] = "done"

    timeline.data.setdefault("outputs", {})
    timeline.data["outputs"]["video"] = str(result.video_path)

    timeline.data.setdefault("render_metadata", {})
    timeline.data["render_metadata"].update(
        {
            "renderer": result.renderer,
            **result.metadata,
        }
    )

    timeline.save(TIMELINE_PATH)

    elapsed = time.perf_counter() - started_at
    logger.info(
        "Stage 5 complete: created video path=%s elapsed=%.2fs",
        result.video_path,
        elapsed,
    )


if __name__ == "__main__":
    run()
