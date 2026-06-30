from __future__ import annotations

from abc import ABC, abstractmethod

from app.prompts.models import ImagePromptRequest, ImagePromptResult


class ImagePromptProvider(ABC):
    provider_name: str

    @abstractmethod
    def build(self, request: ImagePromptRequest) -> ImagePromptResult:
        """Build an image prompt for a planned scene."""
