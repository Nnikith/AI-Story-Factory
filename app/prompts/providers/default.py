from __future__ import annotations

from app.prompts.models import ImagePromptRequest, ImagePromptResult
from app.prompts.providers.base import ImagePromptProvider


class DefaultImagePromptProvider(ImagePromptProvider):
    provider_name = "default"

    def build(self, request: ImagePromptRequest) -> ImagePromptResult:
        prompt = (
            f"{request.style} illustration, "
            "high detail, dramatic lighting, "
            f"mood: {request.mood}, "
            f"scene: {request.scene_text}"
        )

        return ImagePromptResult(
            prompt=prompt,
            negative_prompt="low quality, blurry, distorted, bad anatomy",
            provider=self.provider_name,
            metadata={
                "style": request.style,
                "mood": request.mood,
            },
        )
