from __future__ import annotations

from abc import ABC, abstractmethod

from app.images.models import ImageGenerationRequest, ImageGenerationResult


class ImageEngine(ABC):
    engine_name: str

    @abstractmethod
    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        """Generate an image using a concrete AI backend."""
