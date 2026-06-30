from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MotionRequest:
    scene: dict
    width: int
    height: int
    fps: int


@dataclass(frozen=True)
class MotionResult:
    scene_id: str
    provider: str
    filter_chain: str
    metadata: dict[str, Any] = field(default_factory=dict)
