from __future__ import annotations

from app.renderer.renderers.base import VideoRenderer
from app.renderer.renderers.ffmpeg import FfmpegRenderer


def create_video_renderer(renderer_name: str) -> VideoRenderer:
    normalized = renderer_name.strip().lower()

    if normalized == "ffmpeg":
        return FfmpegRenderer()

    raise ValueError(f"Unsupported video renderer: {renderer_name}")
