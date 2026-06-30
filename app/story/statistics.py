from __future__ import annotations

import re

from app.story.models import StoryStatistics

WORDS_PER_MINUTE = 150


class StoryStatisticsCalculator:
    def calculate(self, text: str, paragraph_count: int) -> StoryStatistics:
        words = self._count_words(text)
        sentences = self._count_sentences(text)
        duration = self._estimate_duration_seconds(words)

        return StoryStatistics(
            word_count=words,
            sentence_count=sentences,
            paragraph_count=paragraph_count,
            estimated_duration_seconds=round(duration, 2),
        )

    def _count_words(self, text: str) -> int:
        return len(re.findall(r"\b[\w'-]+\b", text))

    def _count_sentences(self, text: str) -> int:
        matches = re.findall(r"[^.!?]+[.!?]", text)
        if matches:
            return len(matches)

        return 1 if text.strip() else 0

    def _estimate_duration_seconds(self, word_count: int) -> float:
        return (word_count / WORDS_PER_MINUTE) * 60
