from __future__ import annotations

from app.subtitles.models import (
    SubtitleBlock,
    SubtitleGenerationRequest,
    SubtitleGenerationResult,
)
from app.subtitles.providers.base import SubtitleProvider


class PlaceholderSubtitleProvider(SubtitleProvider):
    provider_name = "placeholder"

    def generate(
        self,
        request: SubtitleGenerationRequest,
    ) -> SubtitleGenerationResult:
        current = 0.0
        blocks: list[SubtitleBlock] = []

        for index, scene in enumerate(request.scenes, start=1):
            duration = _scene_duration_seconds(scene)
            start = current
            end = current + duration
            text = str(scene.get("narration", ""))

            blocks.append(
                SubtitleBlock(
                    index=index,
                    text=text,
                    start_seconds=start,
                    end_seconds=end,
                )
            )

            current = end

        return SubtitleGenerationResult(
            blocks=blocks,
            provider=self.provider_name,
            metadata={
                "mode": "scene_level",
            },
        )


def _scene_duration_seconds(scene: dict) -> float:
    return float(scene.get("duration_seconds") or scene.get("duration") or 6.0)
