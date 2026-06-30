from __future__ import annotations

from app.images.models import ImageGenerationRequest, ImageGenerationResult
from app.images.providers.base import ImageProvider


class LocalAiImageProvider(ImageProvider):
    provider_name = "local_ai"

    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        raise NotImplementedError(
            "Local AI image generation is not implemented yet. "
            "Use images.provider='placeholder' until the SDXL backend is added."
        )
