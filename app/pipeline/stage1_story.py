from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from textwrap import wrap
from app.core.logger import get_logger
import time

ROOT = Path(__file__).resolve().parents[2]

INPUT_STORY = ROOT / "data" / "input" / "story.txt"
OUTPUT_DIR = ROOT / "data" / "output"
TIMELINE_PATH = OUTPUT_DIR / "timeline.json"

logger = get_logger("stage1_story")

def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def split_into_scenes(text: str, max_chars: int = 220) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks: list[str] = []

    for paragraph in paragraphs:
        chunks.extend(wrap(paragraph, width=max_chars, break_long_words=False))

    return chunks or ["No story content found."]


def make_image_prompt(scene_text: str) -> str:
    return (
        "cinematic anime fantasy illustration, "
        "high detail, dramatic lighting, "
        f"scene: {scene_text}"
    )


def build_timeline(story_text: str) -> dict:
    scene_texts = split_into_scenes(story_text)

    scenes = []
    current_time = 0.0

    for index, narration in enumerate(scene_texts, start=1):
        duration = max(5.0, min(10.0, len(narration) / 25))

        scene_id = f"scene_{index:03d}"

        scenes.append(
            {
                "scene_id": scene_id,
                "order": index,
                "duration_seconds": round(duration, 2),
                "start_seconds": round(current_time, 2),
                "end_seconds": round(current_time + duration, 2),
                "narration": narration,
                "image_prompt": make_image_prompt(narration),
                "negative_prompt": "low quality, blurry, distorted, bad anatomy",
                "characters": [],
                "location": None,
                "mood": "fantasy",
                "image_path": f"data/output/images/{scene_id}.png",
                "audio_path": f"data/output/audio/{scene_id}.wav",
                "subtitle_text": narration,
                "subtitle_start": round(current_time, 2),
                "subtitle_end": round(current_time + duration, 2),
                "camera": {
                    "type": "slow_zoom_in",
                    "strength": 0.08,
                },
                "status": {
                    "script": "done",
                    "image": "pending",
                    "voice": "pending",
                    "subtitle": "pending",
                    "render": "pending",
                },
            }
        )

        current_time += duration

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
    logger.info("Stage 1 complete: created timeline=%s elapsed=%.2fs", TIMELINE_PATH, elapsed)


if __name__ == "__main__":
    main()