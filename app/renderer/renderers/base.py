from __future__ import annotations

from abc import ABC, abstractmethod

from app.renderer.models import RenderRequest, RenderResult


class VideoRenderer(ABC):
    renderer_name: str

    @abstractmethod
    def render(self, request: RenderRequest) -> RenderResult:
        """Render a video from timeline data."""
