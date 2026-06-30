from __future__ import annotations

from abc import ABC, abstractmethod

from app.images.models import ImageGenerationRequest, ImageGenerationResult


class ImageProvider(ABC):
    provider_name: str

    @abstractmethod
    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        """Generate an image for a scene."""
