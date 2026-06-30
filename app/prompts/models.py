from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ImagePromptRequest:
    scene_text: str
    mood: str = "fantasy"
    style: str = "cinematic anime fantasy"
    character_prompts: list[str] = field(default_factory=list)
    negative_character_prompts: list[str] = field(default_factory=list)
    location: str | None = None
    time_of_day: str | None = None
    visual_focus: str | None = None


@dataclass(frozen=True)
class ImagePromptResult:
    prompt: str
    negative_prompt: str
    provider: str
    metadata: dict[str, Any] = field(default_factory=dict)
