from __future__ import annotations

import re
from collections import Counter

from app.story.models import StoryCharacter

ROLE_CHARACTER_PATTERNS = {
    "hero": {
        "name": "Hero",
        "description": "young fantasy protagonist",
        "aliases": ["hero", "protagonist", "young hero"],
    },
    "boy": {
        "name": "Boy",
        "description": "young boy",
        "aliases": ["boy", "young boy"],
    },
    "girl": {
        "name": "Girl",
        "description": "young girl",
        "aliases": ["girl", "young girl"],
    },
    "king": {
        "name": "King",
        "description": "royal ruler",
        "aliases": ["king"],
    },
    "queen": {
        "name": "Queen",
        "description": "royal ruler",
        "aliases": ["queen"],
    },
    "princess": {
        "name": "Princess",
        "description": "royal heir",
        "aliases": ["princess"],
    },
    "prince": {
        "name": "Prince",
        "description": "royal heir",
        "aliases": ["prince"],
    },
    "wizard": {
        "name": "Wizard",
        "description": "magic user",
        "aliases": ["wizard"],
    },
    "dragon": {
        "name": "Dragon",
        "description": "mythical creature",
        "aliases": ["dragon"],
    },
    "rider": {
        "name": "Rider",
        "description": "mounted traveler",
        "aliases": ["rider"],
    },
    "riders": {
        "name": "Riders",
        "description": "mounted travelers",
        "aliases": ["riders"],
    },
}


class StoryCharacterExtractor:
    def extract(self, text: str) -> list[StoryCharacter]:
        normalized = text.lower()
        mentions = self._count_role_mentions(normalized)

        characters: list[StoryCharacter] = []

        for role, count in mentions.items():
            if count <= 0:
                continue

            pattern = ROLE_CHARACTER_PATTERNS[role]
            name = pattern["name"]
            description = pattern["description"]

            characters.append(
                StoryCharacter(
                    character_id=self._to_character_id(name),
                    name=name,
                    description=description,
                    visual_prompt=self._build_visual_prompt(name, description),
                    negative_prompt=self._build_negative_prompt(name),
                    aliases=pattern["aliases"],
                    mention_count=count,
                )
            )

        return sorted(
            characters,
            key=lambda character: (-character.mention_count, character.character_id),
        )

    def _count_role_mentions(self, text: str) -> Counter[str]:
        mentions: Counter[str] = Counter()

        for role in ROLE_CHARACTER_PATTERNS:
            pattern = rf"\b{re.escape(role)}\b"
            mentions[role] = len(re.findall(pattern, text))

        return mentions

    def _to_character_id(self, name: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
        return normalized or "character"

    def _build_visual_prompt(self, name: str, description: str) -> str:
        return f"{description}, consistent character design, {name}"

    def _build_negative_prompt(self, name: str) -> str:
        return f"inconsistent {name}, different face, duplicate character"
