from __future__ import annotations

import re
from textwrap import wrap


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
        chunks = self._group_sentences(sentences, max_chars=max_chars)

        if chunks:
            return chunks

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

    def _group_sentences(self, sentences: list[str], max_chars: int) -> list[str]:
        chunks: list[str] = []
        current: list[str] = []
        current_length = 0

        for sentence in sentences:
            projected_length = current_length + len(sentence) + (1 if current else 0)

            if current and projected_length > max_chars:
                chunks.append(" ".join(current))
                current = [sentence]
                current_length = len(sentence)
            else:
                current.append(sentence)
                current_length = projected_length

        if current:
            chunks.append(" ".join(current))

        return chunks
