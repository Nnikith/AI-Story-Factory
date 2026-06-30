from __future__ import annotations

import time
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.core.timeline import Timeline
from app.motion import MotionRequest, create_motion_provider
from app.renderer import RenderRequest, create_video_renderer

TIMELINE_PATH = Path("data/output/timeline.json")
SUBTITLE_PATH = Path("data/output/subtitles/subtitles.srt")
VIDEO_PATH = Path("data/output/videos/demo.mp4")

logger = get_logger("stage5_video")


def _parse_resolution(resolution: str) -> tuple[int, int]:
    width_text, height_text = resolution.lower().split("x", maxsplit=1)
    return int(width_text), int(height_text)


def _scene_id(scene: dict) -> str:
    return str(scene.get("scene_id") or scene.get("id"))


def run() -> None:
    logger.info("Starting Stage 5 video render")
    started_at = time.perf_counter()

    timeline = Timeline.load(TIMELINE_PATH)
    renderer = create_video_renderer("ffmpeg")

    width, height = _parse_resolution(settings.render.resolution)
    motion_filters: dict[str, str] = {}

    if settings.motion.enabled:
        motion_provider = create_motion_provider(settings.motion.provider)

        for scene in timeline.scenes:
            request = MotionRequest(
                scene=scene,
                width=width,
                height=height,
                fps=settings.render.fps,
            )
            result = motion_provider.build_filter(request)
            motion_filters[result.scene_id] = result.filter_chain

            scene.setdefault("motion_metadata", {})
            scene["motion_metadata"].update(
                {
                    "provider": result.provider,
                    **result.metadata,
                }
            )

    request = RenderRequest(
        timeline_data=timeline.data,
        output_path=VIDEO_PATH,
        subtitle_path=SUBTITLE_PATH,
        resolution=settings.render.resolution,
        fps=settings.render.fps,
        codec=settings.render.codec,
        crf=settings.render.crf,
        preset=settings.render.preset,
        motion_filters=motion_filters,
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
