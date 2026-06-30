from __future__ import annotations

from abc import ABC, abstractmethod

from app.voice.models import VoiceGenerationRequest, VoiceGenerationResult


class VoiceProvider(ABC):
    provider_name: str

    @abstractmethod
    def generate(self, request: VoiceGenerationRequest) -> VoiceGenerationResult:
        """Generate narration audio for a scene."""
