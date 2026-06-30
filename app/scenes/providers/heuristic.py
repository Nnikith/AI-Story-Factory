from __future__ import annotations

from textwrap import wrap

from app.scenes.models import (
    PlannedScene,
    ScenePlanningRequest,
    ScenePlanningResult,
)
from app.scenes.providers.base import ScenePlanner


class HeuristicScenePlanner(ScenePlanner):
    provider_name = "heuristic"

    def plan(self, request: ScenePlanningRequest) -> ScenePlanningResult:
        scene_texts = _split_into_scenes(
            request.story_text,
            max_chars=request.max_scene_chars,
        )

        scenes: list[PlannedScene] = []
        current_time = 0.0

        for index, narration in enumerate(scene_texts, start=1):
            duration = max(5.0, min(10.0, len(narration) / 25))
            scene_id = f"scene_{index:03d}"
            start = round(current_time, 2)
            end = round(current_time + duration, 2)

            scenes.append(
                PlannedScene(
                    scene_id=scene_id,
                    order=index,
                    narration=narration,
                    duration_seconds=round(duration, 2),
                    start_seconds=start,
                    end_seconds=end,
                    image_prompt=_make_image_prompt(narration),
                    negative_prompt="low quality, blurry, distorted, bad anatomy",
                    characters=[],
                    location=None,
                    mood="fantasy",
                    camera={
                        "type": "slow_zoom_in",
                        "strength": 0.08,
                    },
                )
            )

            current_time += duration

        return ScenePlanningResult(
            scenes=scenes,
            provider=self.provider_name,
            metadata={
                "max_scene_chars": request.max_scene_chars,
                "scene_count": len(scenes),
            },
        )


def _split_into_scenes(text: str, max_chars: int) -> list[str]:
    paragraphs = [paragraph.strip() for paragraph in text.split("\n") if paragraph.strip()]
    chunks: list[str] = []

    for paragraph in paragraphs:
        chunks.extend(
            wrap(
                paragraph,
                width=max_chars,
                break_long_words=False,
            )
        )

    return chunks or ["No story content found."]


def _make_image_prompt(scene_text: str) -> str:
    return (
        "cinematic anime fantasy illustration, "
        "high detail, dramatic lighting, "
        f"scene: {scene_text}"
    )
