from __future__ import annotations

import re


class StoryCleaner:
    def clean(self, text: str) -> str:
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        normalized = self._normalize_quotes(normalized)
        normalized = self._trim_lines(normalized)
        normalized = re.sub(r"\n{3,}", "\n\n", normalized)
        return normalized.strip()

    def _trim_lines(self, text: str) -> str:
        return "\n".join(line.strip() for line in text.split("\n"))

    def _normalize_quotes(self, text: str) -> str:
        replacements = {
            "\u201c": '"',
            "\u201d": '"',
            "\u2018": "'",
            "\u2019": "'",
        }

        for source, target in replacements.items():
            text = text.replace(source, target)

        return text
