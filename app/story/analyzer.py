from __future__ import annotations

from app.story.characters import StoryCharacterExtractor
from app.story.cleaner import StoryCleaner
from app.story.models import StoryAnalysis, StoryParagraph
from app.story.statistics import StoryStatisticsCalculator


class StoryAnalyzer:
    def __init__(
        self,
        cleaner: StoryCleaner | None = None,
        statistics_calculator: StoryStatisticsCalculator | None = None,
        character_extractor: StoryCharacterExtractor | None = None,
    ) -> None:
        self.cleaner = cleaner or StoryCleaner()
        self.statistics_calculator = (
            statistics_calculator or StoryStatisticsCalculator()
        )
        self.character_extractor = character_extractor or StoryCharacterExtractor()

    def analyze(self, text: str) -> StoryAnalysis:
        clean_text = self.cleaner.clean(text)
        paragraphs = self._extract_paragraphs(clean_text)
        statistics = self.statistics_calculator.calculate(
            clean_text,
            paragraph_count=len(paragraphs),
        )
        characters = self.character_extractor.extract(clean_text)

        return StoryAnalysis(
            clean_text=clean_text,
            paragraphs=paragraphs,
            statistics=statistics,
            characters=characters,
        )

    def _extract_paragraphs(self, text: str) -> list[StoryParagraph]:
        raw_paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        return [
            StoryParagraph(
                index=index,
                text=paragraph,
                has_dialogue=self._has_dialogue(paragraph),
            )
            for index, paragraph in enumerate(raw_paragraphs, start=1)
        ]

    def _has_dialogue(self, text: str) -> bool:
        return '"' in text or "'" in text
