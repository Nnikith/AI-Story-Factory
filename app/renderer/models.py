from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RenderRequest:
    timeline_data: dict
    output_path: Path
    subtitle_path: Path
    resolution: str
    fps: int
    codec: str
    crf: int
    preset: str
    motion_filters: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RenderResult:
    video_path: Path
    renderer: str
    metadata: dict[str, Any] = field(default_factory=dict)
