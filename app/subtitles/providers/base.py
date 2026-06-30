from __future__ import annotations

from abc import ABC, abstractmethod

from app.subtitles.models import SubtitleGenerationRequest, SubtitleGenerationResult


class SubtitleProvider(ABC):
    provider_name: str

    @abstractmethod
    def generate(
        self,
        request: SubtitleGenerationRequest,
    ) -> SubtitleGenerationResult:
        """Generate subtitle blocks from timeline scenes."""
