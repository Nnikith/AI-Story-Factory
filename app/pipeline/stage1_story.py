from __future__ import annotations

import json
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.scenes import ScenePlanningRequest, create_scene_planner

ROOT = Path(__file__).resolve().parents[2]

INPUT_STORY = ROOT / "data" / "input" / "story.txt"
OUTPUT_DIR = ROOT / "data" / "output"
TIMELINE_PATH = OUTPUT_DIR / "timeline.json"

logger = get_logger("stage1_story")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scene_to_timeline_dict(scene) -> dict:
    scene_data = asdict(scene)

    scene_data.update(
        {
            "image_path": f"data/output/images/{scene.scene_id}.png",
            "audio_path": f"data/output/audio/{scene.scene_id}.wav",
            "subtitle_text": scene.narration,
            "subtitle_start": scene.start_seconds,
            "subtitle_end": scene.end_seconds,
            "status": {
                "script": "done",
                "image": "pending",
                "voice": "pending",
                "subtitle": "pending",
                "render": "pending",
            },
        }
    )

    return scene_data


def build_timeline(story_text: str) -> dict:
    planner = create_scene_planner(settings.scene_planning.provider)

    planning_result = planner.plan(
        ScenePlanningRequest(
            story_text=story_text,
            max_scene_chars=settings.scene_planning.max_scene_chars,
        )
    )

    scenes = [_scene_to_timeline_dict(scene) for scene in planning_result.scenes]

    return {
        "project": {
            "name": "AI Story Factory Demo",
            "version": "0.0.1",
            "created_at": now_utc(),
        },
        "source": {
            "type": "story_text",
            "path": str(INPUT_STORY.relative_to(ROOT)),
            "title": "Demo Story",
            "language": "en",
        },
        "settings": {
            "aspect_ratio": "16:9",
            "resolution": "1920x1080",
            "fps": 30,
            "subtitle_style": "default",
            "image_style": "cinematic anime fantasy",
            "voice": "default",
        },
        "characters": [],
        "scenes": scenes,
        "assets": {
            "music": None,
            "font": None,
        },
        "outputs": {
            "timeline": str(TIMELINE_PATH.relative_to(ROOT)),
            "video": "data/output/videos/demo.mp4",
            "subtitles": "data/output/subtitles/subtitles.srt",
            "metadata": "data/output/metadata/youtube.json",
        },
        "run": {
            "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "started_at": now_utc(),
            "completed_at": now_utc(),
            "errors": [],
            "warnings": [],
        },
        "scene_planning_metadata": {
            "provider": planning_result.provider,
            **planning_result.metadata,
        },
    }


def main() -> None:
    started_at = time.perf_counter()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT_STORY.exists():
        raise FileNotFoundError(f"Missing input story: {INPUT_STORY}")

    story_text = INPUT_STORY.read_text(encoding="utf-8").strip()
    timeline = build_timeline(story_text)

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
