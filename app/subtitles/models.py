from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SubtitleBlock:
    index: int
    text: str
    start_seconds: float
    end_seconds: float


@dataclass(frozen=True)
class SubtitleGenerationRequest:
    scenes: list[dict]
    max_lines: int
    max_chars_per_line: int


@dataclass(frozen=True)
class SubtitleGenerationResult:
    blocks: list[SubtitleBlock]
    provider: str
    metadata: dict[str, Any] = field(default_factory=dict)
