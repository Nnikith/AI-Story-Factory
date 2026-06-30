from __future__ import annotations

import re

from app.prompts import ImagePromptRequest, create_image_prompt_provider
from app.scenes.models import (
    PlannedScene,
    ScenePlanningRequest,
    ScenePlanningResult,
)
from app.scenes.providers.base import ScenePlanner
from app.scenes.splitter import SceneSplitter
from app.story.models import StoryCharacter


class HeuristicScenePlanner(ScenePlanner):
    provider_name = "heuristic"

    def __init__(self, splitter: SceneSplitter | None = None) -> None:
        self.splitter = splitter or SceneSplitter()

    def plan(self, request: ScenePlanningRequest) -> ScenePlanningResult:
        scene_texts = self.splitter.split(
            request.story_text,
            max_chars=request.max_scene_chars,
        )
        prompt_provider = create_image_prompt_provider(request.image_prompt_provider)

        scenes: list[PlannedScene] = []
        current_time = 0.0

        for index, narration in enumerate(scene_texts, start=1):
            duration = self._estimate_duration_seconds(narration)
            scene_id = f"scene_{index:03d}"
            start = round(current_time, 2)
            end = round(current_time + duration, 2)
            mood = "fantasy"
            scene_characters = self._assign_scene_characters(request, narration)

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
                    characters=scene_characters,
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
                "splitter": "narrative_beat",
                "story_analysis_available": request.story_analysis is not None,
                "detected_character_count": (
                    len(request.story_analysis.characters)
                    if request.story_analysis is not None
                    else 0
                ),
            },
        )

    def _assign_scene_characters(
        self,
        request: ScenePlanningRequest,
        narration: str,
    ) -> list[str]:
        if request.story_analysis is None:
            return []

        matched_ids = [
            character.character_id
            for character in request.story_analysis.characters
            if self._character_appears(character, narration)
        ]

        return matched_ids

    def _character_appears(
        self,
        character: StoryCharacter,
        narration: str,
    ) -> bool:
        normalized = narration.lower()
        candidates = [character.name, *character.aliases]

        return any(
            re.search(rf"\b{re.escape(candidate.lower())}\b", normalized)
            for candidate in candidates
        )

    def _estimate_duration_seconds(self, narration: str) -> float:
        return max(5.0, min(10.0, len(narration) / 25))
