from __future__ import annotations

from app.prompts.providers.base import ImagePromptProvider
from app.prompts.providers.default import DefaultImagePromptProvider


def create_image_prompt_provider(provider_name: str) -> ImagePromptProvider:
    normalized = provider_name.strip().lower()

    if normalized in {"default", "heuristic", "simple"}:
        return DefaultImagePromptProvider()

    raise ValueError(f"Unsupported image prompt provider: {provider_name}")
