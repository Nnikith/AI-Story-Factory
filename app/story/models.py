from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StoryParagraph:
    index: int
    text: str
    has_dialogue: bool


@dataclass(frozen=True)
class StoryStatistics:
    word_count: int
    sentence_count: int
    paragraph_count: int
    estimated_duration_seconds: float


@dataclass(frozen=True)
class StoryAnalysis:
    clean_text: str
    paragraphs: list[StoryParagraph]
    statistics: StoryStatistics
