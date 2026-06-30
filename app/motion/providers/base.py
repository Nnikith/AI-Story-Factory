from __future__ import annotations

from abc import ABC, abstractmethod

from app.motion.models import MotionRequest, MotionResult


class MotionProvider(ABC):
    provider_name: str

    @abstractmethod
    def build_filter(self, request: MotionRequest) -> MotionResult:
        """Build a video filter chain for one scene."""
