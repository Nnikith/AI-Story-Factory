from __future__ import annotations

from app.subtitles.providers.base import SubtitleProvider
from app.subtitles.providers.placeholder import PlaceholderSubtitleProvider


def create_subtitle_provider(provider_name: str) -> SubtitleProvider:
    normalized = provider_name.strip().lower()

    if normalized == "placeholder":
        return PlaceholderSubtitleProvider()

    raise ValueError(f"Unsupported subtitle provider: {provider_name}")
