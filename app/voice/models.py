from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class VoiceGenerationRequest:
    scene_id: str
    text: str
    output_path: Path
    duration_seconds: float
    sample_rate: int = 24000
    voice_name: str = "default"
    force: bool = False


@dataclass(frozen=True)
class VoiceGenerationResult:
    scene_id: str
    audio_path: Path
    provider: str
    duration_seconds: float
    cached: bool = False
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
