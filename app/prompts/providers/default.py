from __future__ import annotations

from app.prompts.compressor import PromptCompressor
from app.prompts.models import ImagePromptRequest, ImagePromptResult
from app.prompts.providers.base import ImagePromptProvider


class DefaultImagePromptProvider(ImagePromptProvider):
    provider_name = "default"

    def __init__(
        self,
        compressor: PromptCompressor | None = None,
        max_prompt_words: int = 55,
    ) -> None:
        self.compressor = compressor or PromptCompressor()
        self.max_prompt_words = max_prompt_words

    def build(self, request: ImagePromptRequest) -> ImagePromptResult:
        character_text = self._build_character_text(request.character_prompts)
        raw_prompt = self._build_raw_prompt(request, character_text)
        compression = self.compressor.compress(
            raw_prompt,
            max_words=self.max_prompt_words,
        )

        negative_prompt = self._build_negative_prompt(
            request.negative_character_prompts
        )

        return ImagePromptResult(
            prompt=compression.prompt,
            negative_prompt=negative_prompt,
            provider=self.provider_name,
            metadata={
                "style": request.style,
                "mood": request.mood,
                "character_prompt_count": len(request.character_prompts),
                "has_location": request.location is not None,
                "has_time_of_day": request.time_of_day is not None,
                "has_visual_focus": request.visual_focus is not None,
                "prompt_compressed": compression.compressed,
                "original_word_count": compression.original_word_count,
                "compressed_word_count": compression.compressed_word_count,
                "max_prompt_words": self.max_prompt_words,
            },
        )

    def _build_raw_prompt(
        self,
        request: ImagePromptRequest,
        character_text: str,
    ) -> str:
        prompt_parts = [
            f"{request.style} illustration",
            "high detail",
            "dramatic lighting",
            f"mood: {request.mood}",
        ]

        if request.location:
            prompt_parts.append(f"location: {request.location}")

        if request.time_of_day:
            prompt_parts.append(f"time of day: {request.time_of_day}")

        if request.visual_focus:
            prompt_parts.append(f"visual focus: {request.visual_focus}")

        if character_text:
            prompt_parts.append(f"characters: {character_text}")

        prompt_parts.append(f"scene: {request.scene_text}")

        return ", ".join(prompt_parts)

    def _build_negative_prompt(
        self,
        negative_character_prompts: list[str],
    ) -> str:
        negative_parts = [
            "low quality",
            "blurry",
            "distorted",
            "bad anatomy",
            *negative_character_prompts,
        ]

        return ", ".join(dict.fromkeys(negative_parts))

    def _build_character_text(self, character_prompts: list[str]) -> str:
        return "; ".join(prompt for prompt in character_prompts if prompt.strip())
