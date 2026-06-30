from __future__ import annotations

from app.images.engines import DiffusersEngine
from app.images.models import ImageGenerationRequest, ImageGenerationResult
from app.images.providers.base import ImageProvider


class LocalAiImageProvider(ImageProvider):
    provider_name = "local_ai"

    def __init__(self) -> None:
        self.engine = DiffusersEngine()

    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        return self.engine.generate(request)
