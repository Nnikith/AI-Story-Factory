from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ImageGenerationRequest:
    scene_id: str
    prompt: str
    negative_prompt: str
    output_path: Path
    width: int
    height: int
    seed: int | None = None
    force: bool = False


@dataclass(frozen=True)
class ImageGenerationResult:
    scene_id: str
    image_path: Path
    provider: str
    cached: bool = False
    seed: int | None = None
    error: str | None = None
