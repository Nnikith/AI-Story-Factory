from __future__ import annotations

import time
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.core.timeline import Timeline
from app.subtitles import SubtitleBlock, SubtitleGenerationRequest, create_subtitle_provider

TIMELINE_PATH = Path("data/output/timeline.json")
SUBTITLE_PATH = Path("data/output/subtitles/subtitles.srt")

logger = get_logger("stage4_subtitles")


def _format_srt_time(seconds: float) -> str:
    ms_total = int(seconds * 1000)
    hours = ms_total // 3_600_000
    ms_total %= 3_600_000
    minutes = ms_total // 60_000
    ms_total %= 60_000
    secs = ms_total // 1000
    millis = ms_total % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def _render_srt(blocks: list[SubtitleBlock]) -> str:
    rendered: list[str] = []

    for block in blocks:
        rendered.append(
            f"{block.index}\n"
            f"{_format_srt_time(block.start_seconds)} --> "
            f"{_format_srt_time(block.end_seconds)}\n"
            f"{block.text}\n"
        )

    return "\n".join(rendered)


def run() -> None:
    logger.info("Starting Stage 4 subtitle generation")
    started_at = time.perf_counter()

    timeline = Timeline.load(TIMELINE_PATH)
    SUBTITLE_PATH.parent.mkdir(parents=True, exist_ok=True)

    provider = create_subtitle_provider(settings.subtitles.provider)

    request = SubtitleGenerationRequest(
        scenes=timeline.scenes,
        max_lines=settings.subtitles.max_lines,
        max_chars_per_line=settings.subtitles.max_chars_per_line,
    )

    result = provider.generate(request)
    SUBTITLE_PATH.write_text(_render_srt(result.blocks), encoding="utf-8")

    scene_blocks: dict[str, list[dict]] = {}

    for scene in timeline.scenes:
        scene_id = str(scene.get("scene_id") or scene.get("id"))
        scene_blocks[scene_id] = []

    for block in result.blocks:
        for scene in timeline.scenes:
            scene_start = float(scene.get("start_seconds", 0.0))
            scene_end = float(scene.get("end_seconds", scene_start + scene.get("duration_seconds", 6.0)))

            if scene_start <= block.start_seconds < scene_end:
                scene_id = str(scene.get("scene_id") or scene.get("id"))
                scene_blocks[scene_id].append(
                    {
                        "index": block.index,
                        "text": block.text,
                        "start_seconds": block.start_seconds,
                        "end_seconds": block.end_seconds,
                    }
                )
                break

    for scene in timeline.scenes:
        scene_id = str(scene.get("scene_id") or scene.get("id"))
        blocks = scene_blocks.get(scene_id, [])

        if blocks:
            scene["subtitle_text"] = "\n".join(block["text"] for block in blocks)
            scene["subtitle_start"] = blocks[0]["start_seconds"]
            scene["subtitle_end"] = blocks[-1]["end_seconds"]
            scene["subtitles"] = blocks

        scene.setdefault("subtitle_metadata", {})
        scene["subtitle_metadata"].update(
            {
                "provider": result.provider,
                **result.metadata,
            }
        )
        scene.setdefault("status", {})["subtitle"] = "done"

        logger.info(
            "Created subtitles for scene=%s blocks=%s",
            scene_id,
            len(blocks),
        )

    timeline.data.setdefault("outputs", {})
    timeline.data["outputs"]["subtitles"] = str(SUBTITLE_PATH)

    timeline.save(TIMELINE_PATH)

    elapsed = time.perf_counter() - started_at
    logger.info(
        "Stage 4 complete: created subtitles path=%s blocks=%s elapsed=%.2fs",
        SUBTITLE_PATH,
        len(result.blocks),
        elapsed,
    )


if __name__ == "__main__":
    run()
