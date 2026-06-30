from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptCompressionResult:
    prompt: str
    original_word_count: int
    compressed_word_count: int
    compressed: bool


class PromptCompressor:
    def compress(
        self,
        prompt: str,
        max_words: int = 55,
    ) -> PromptCompressionResult:
        clean_prompt = self._normalize_prompt(prompt)
        original_word_count = self._count_words(clean_prompt)

        if original_word_count <= max_words:
            return PromptCompressionResult(
                prompt=clean_prompt,
                original_word_count=original_word_count,
                compressed_word_count=original_word_count,
                compressed=False,
            )

        compressed_prompt = self._compress_by_sections(
            clean_prompt,
            max_words=max_words,
        )

        return PromptCompressionResult(
            prompt=compressed_prompt,
            original_word_count=original_word_count,
            compressed_word_count=self._count_words(compressed_prompt),
            compressed=True,
        )

    def _normalize_prompt(self, prompt: str) -> str:
        sections = [
            section.strip()
            for section in prompt.replace("\n", " ").split(",")
            if section.strip()
        ]

        return ", ".join(sections)

    def _compress_by_sections(self, prompt: str, max_words: int) -> str:
        sections = [
            section.strip()
            for section in prompt.split(",")
            if section.strip()
        ]

        kept_sections: list[str] = []
        current_words = 0

        for section in sections:
            section_words = self._count_words(section)

            if kept_sections and current_words + section_words > max_words:
                break

            kept_sections.append(section)
            current_words += section_words

        return ", ".join(kept_sections)

    def _count_words(self, text: str) -> int:
        return len(text.split())
