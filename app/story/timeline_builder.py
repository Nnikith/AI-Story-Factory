from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from app.scenes.models import ScenePlanningResult
from app.story.models import StoryCharacter


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class TimelineBuilder:
    def __init__(
        self,
        project_root: Path,
        input_story_path: Path,
        timeline_path: Path,
    ) -> None:
        self.project_root = project_root
        self.input_story_path = input_story_path
        self.timeline_path = timeline_path

    def build(
        self,
        planning_result: ScenePlanningResult,
        characters: list[StoryCharacter] | None = None,
    ) -> dict:
        scenes = [
            self._scene_to_timeline_dict(scene)
            for scene in planning_result.scenes
        ]

        return {
            "project": {
                "name": "AI Story Factory Demo",
                "version": "0.0.1",
                "created_at": now_utc(),
            },
            "source": {
                "type": "story_text",
                "path": str(self.input_story_path.relative_to(self.project_root)),
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
            "characters": [asdict(character) for character in characters or []],
            "scenes": scenes,
            "assets": {
                "music": None,
                "font": None,
            },
            "outputs": {
                "timeline": str(self.timeline_path.relative_to(self.project_root)),
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

    @staticmethod
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
