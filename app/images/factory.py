from __future__ import annotations

from app.images.providers.base import ImageProvider
from app.images.providers.local_ai import LocalAiImageProvider
from app.images.providers.placeholder import PlaceholderImageProvider


def create_image_provider(provider_name: str) -> ImageProvider:
    normalized = provider_name.strip().lower()

    if normalized == "placeholder":
        return PlaceholderImageProvider()

    if normalized in {"local_ai", "local-ai", "local"}:
        return LocalAiImageProvider()

    raise ValueError(f"Unsupported image provider: {provider_name}")
