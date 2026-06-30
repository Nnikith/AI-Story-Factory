from __future__ import annotations

from textwrap import wrap

from app.prompts import ImagePromptRequest, create_image_prompt_provider
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
        prompt_provider = create_image_prompt_provider(request.image_prompt_provider)

        scenes: list[PlannedScene] = []
        current_time = 0.0

        for index, narration in enumerate(scene_texts, start=1):
            duration = max(5.0, min(10.0, len(narration) / 25))
            scene_id = f"scene_{index:03d}"
            start = round(current_time, 2)
            end = round(current_time + duration, 2)
            mood = "fantasy"

            prompt_result = prompt_provider.build(
                ImagePromptRequest(
                    scene_text=narration,
                    mood=mood,
                    style=request.image_prompt_style,
                )
            )

            scenes.append(
                PlannedScene(
                    scene_id=scene_id,
                    order=index,
                    narration=narration,
                    duration_seconds=round(duration, 2),
                    start_seconds=start,
                    end_seconds=end,
                    image_prompt=prompt_result.prompt,
                    negative_prompt=prompt_result.negative_prompt,
                    characters=[],
                    location=None,
                    mood=mood,
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
                "image_prompt_provider": request.image_prompt_provider,
                "image_prompt_style": request.image_prompt_style,
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
