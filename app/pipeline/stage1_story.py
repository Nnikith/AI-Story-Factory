from __future__ import annotations

import json
import time
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.scenes import ScenePlanningRequest, create_scene_planner
from app.scenes import ScenePlanningRequest, create_scene_planner
from app.story import StoryAnalyzer
from app.story.timeline_builder import TimelineBuilder
from app.story.timeline_builder import TimelineBuilder

ROOT = Path(__file__).resolve().parents[2]

INPUT_STORY = ROOT / "data" / "input" / "story.txt"
OUTPUT_DIR = ROOT / "data" / "output"
TIMELINE_PATH = OUTPUT_DIR / "timeline.json"

logger = get_logger("stage1_story")


def main() -> None:
    started_at = time.perf_counter()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT_STORY.exists():
        raise FileNotFoundError(f"Missing input story: {INPUT_STORY}")

    story_text = INPUT_STORY.read_text(encoding="utf-8")
    analysis = StoryAnalyzer().analyze(story_text)

    logger.info(
        "Story analyzed: words=%s sentences=%s paragraphs=%s estimated_duration=%.2fs",
        analysis.statistics.word_count,
        analysis.statistics.sentence_count,
        analysis.statistics.paragraph_count,
        analysis.statistics.estimated_duration_seconds,
    )

    planner = create_scene_planner(settings.scene_planning.provider)
    planning_result = planner.plan(
        ScenePlanningRequest(
            story_text=analysis.clean_text,
            max_scene_chars=settings.scene_planning.max_scene_chars,
            image_prompt_style=settings.prompts.image_style,
            image_prompt_provider=settings.prompts.image_provider,
        )
    )

    builder = TimelineBuilder(
        project_root=ROOT,
        input_story_path=INPUT_STORY,
        timeline_path=TIMELINE_PATH,
    )

    timeline = builder.build(planning_result)

    TIMELINE_PATH.write_text(
        json.dumps(timeline, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    elapsed = time.perf_counter() - started_at
    logger.info(
        "Stage 1 complete: created timeline=%s elapsed=%.2fs",
        TIMELINE_PATH,
        elapsed,
    )


if __name__ == "__main__":
    main()
