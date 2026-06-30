from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SceneContext:
    location: str | None
    time_of_day: str | None
    visual_focus: str | None


class SceneContextAnalyzer:
    LOCATION_KEYWORDS = {
        "village": "village",
        "forest": "forest",
        "castle": "castle",
        "kingdom": "kingdom",
        "temple": "ancient temple",
        "cave": "cave",
        "mountain": "mountain",
        "river": "river",
        "city": "city",
        "battlefield": "battlefield",
    }

    TIME_KEYWORDS = {
        "dawn": "dawn",
        "morning": "morning",
        "sunset": "sunset",
        "dusk": "dusk",
        "night": "night",
        "midnight": "midnight",
    }

    def analyze(self, narration: str) -> SceneContext:
        normalized = narration.lower()

        return SceneContext(
            location=self._find_first_match(normalized, self.LOCATION_KEYWORDS),
            time_of_day=self._find_first_match(normalized, self.TIME_KEYWORDS),
            visual_focus=self._infer_visual_focus(narration),
        )

    def _find_first_match(
        self,
        text: str,
        patterns: dict[str, str],
    ) -> str | None:
        for keyword, value in patterns.items():
            if keyword in text:
                return value

        return None

    def _infer_visual_focus(self, narration: str) -> str | None:
        sentence = narration.strip()
        if not sentence:
            return None

        return sentence.split(".")[0].strip()
