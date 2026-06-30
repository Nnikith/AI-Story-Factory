from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.story.models import StoryAnalysis


@dataclass(frozen=True)
class ScenePlanningRequest:
    story_text: str
    max_scene_chars: int = 220
    image_prompt_style: str = "cinematic anime fantasy"
    image_prompt_provider: str = "default"
    story_analysis: StoryAnalysis | None = None


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
    time_of_day: str | None = None
    visual_focus: str | None = None


@dataclass(frozen=True)
class ScenePlanningResult:
    scenes: list[PlannedScene]
    provider: str
    metadata: dict[str, Any] = field(default_factory=dict)
