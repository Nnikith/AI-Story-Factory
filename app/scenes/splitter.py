from __future__ import annotations

import re
from textwrap import wrap

BEAT_STARTERS = (
    "after ",
    "afterward",
    "as ",
    "at dawn",
    "at dusk",
    "at midnight",
    "at night",
    "at sunset",
    "before ",
    "by morning",
    "finally",
    "hours later",
    "later",
    "meanwhile",
    "moments later",
    "soon",
    "suddenly",
    "that morning",
    "that night",
    "then",
    "when ",
)


class SceneSplitter:
    def split(self, text: str, max_chars: int) -> list[str]:
        paragraphs = self._extract_paragraphs(text)
        chunks: list[str] = []

        for paragraph in paragraphs:
            chunks.extend(self._split_paragraph(paragraph, max_chars=max_chars))

        return chunks or ["No story content found."]

    def _extract_paragraphs(self, text: str) -> list[str]:
        return [
            paragraph.strip()
            for paragraph in re.split(r"\n\s*\n|\n", text)
            if paragraph.strip()
        ]

    def _split_paragraph(self, paragraph: str, max_chars: int) -> list[str]:
        if len(paragraph) <= max_chars:
            return [paragraph]

        sentences = self._split_sentences(paragraph)
        beat_chunks = self._group_by_story_beats(sentences, max_chars=max_chars)

        if beat_chunks:
            return beat_chunks

        sentence_chunks = self._group_sentences(sentences, max_chars=max_chars)

        if sentence_chunks:
            return sentence_chunks

        return wrap(
            paragraph,
            width=max_chars,
            break_long_words=False,
        )

    def _split_sentences(self, text: str) -> list[str]:
        return [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", text)
            if sentence.strip()
        ]

    def _group_by_story_beats(
        self,
        sentences: list[str],
        max_chars: int,
    ) -> list[str]:
        if len(sentences) <= 1:
            return []

        chunks: list[str] = []
        current: list[str] = []

        for sentence in sentences:
            if current and self._starts_new_beat(sentence):
                chunks.append(" ".join(current))
                current = [sentence]
                continue

            projected = self._projected_length(current, sentence)

            if current and projected > max_chars:
                chunks.append(" ".join(current))
                current = [sentence]
            else:
                current.append(sentence)

        if current:
            chunks.append(" ".join(current))

        if len(chunks) <= 1:
            return []

        return chunks

    def _starts_new_beat(self, sentence: str) -> bool:
        normalized = sentence.strip().lower()
        return any(normalized.startswith(starter) for starter in BEAT_STARTERS)

    def _group_sentences(self, sentences: list[str], max_chars: int) -> list[str]:
        chunks: list[str] = []
        current: list[str] = []

        for sentence in sentences:
            projected_length = self._projected_length(current, sentence)

            if current and projected_length > max_chars:
                chunks.append(" ".join(current))
                current = [sentence]
            else:
                current.append(sentence)

        if current:
            chunks.append(" ".join(current))

        return chunks

    def _projected_length(self, current: list[str], sentence: str) -> int:
        return sum(len(item) for item in current) + len(sentence) + len(current)
