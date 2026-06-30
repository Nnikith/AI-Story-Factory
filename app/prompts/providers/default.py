from __future__ import annotations

from app.prompts.models import ImagePromptRequest, ImagePromptResult
from app.prompts.providers.base import ImagePromptProvider


class DefaultImagePromptProvider(ImagePromptProvider):
    provider_name = "default"

    def build(self, request: ImagePromptRequest) -> ImagePromptResult:
        character_text = self._build_character_text(request.character_prompts)

        prompt_parts = [
            f"{request.style} illustration",
            "high detail",
            "dramatic lighting",
            f"mood: {request.mood}",
        ]

        if character_text:
            prompt_parts.append(f"characters: {character_text}")

        prompt_parts.append(f"scene: {request.scene_text}")

        negative_parts = [
            "low quality",
            "blurry",
            "distorted",
            "bad anatomy",
            *request.negative_character_prompts,
        ]

        return ImagePromptResult(
            prompt=", ".join(prompt_parts),
            negative_prompt=", ".join(dict.fromkeys(negative_parts)),
            provider=self.provider_name,
            metadata={
                "style": request.style,
                "mood": request.mood,
                "character_prompt_count": len(request.character_prompts),
            },
        )

    def _build_character_text(self, character_prompts: list[str]) -> str:
        return "; ".join(prompt for prompt in character_prompts if prompt.strip())
