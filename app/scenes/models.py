from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ScenePlanningRequest:
    story_text: str
    max_scene_chars: int = 220


@dataclass(frozen=True)
class PlannedScene:
    scene_id: str
    order: int
    narration: str
    duration_seconds: float
    start_seconds: float
    end_seconds: float
    image_prompt: str
    negative_prompt: str
    characters: list[str]
    location: str | None
    mood: str
    camera: dict[str, Any]


@dataclass(frozen=True)
class ScenePlanningResult:
    scenes: list[PlannedScene]
    provider: str
    metadata: dict[str, Any] = field(default_factory=dict)
