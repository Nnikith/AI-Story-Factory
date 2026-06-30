from __future__ import annotations

from app.subtitles.models import (
    SubtitleBlock,
    SubtitleGenerationRequest,
    SubtitleGenerationResult,
)
from app.subtitles.providers.base import SubtitleProvider


class PlaceholderSubtitleProvider(SubtitleProvider):
    provider_name = "placeholder"

    def generate(
        self,
        request: SubtitleGenerationRequest,
    ) -> SubtitleGenerationResult:
        global_index = 1
        current_time = 0.0
        blocks: list[SubtitleBlock] = []

        for scene in request.scenes:
            duration = _scene_duration_seconds(scene)
            scene_start = current_time
            scene_end = scene_start + duration

            chunks = _split_text(
                text=str(scene.get("narration", "")),
                max_chars=request.max_chars_per_line,
            )

            if not chunks:
                current_time = scene_end
                continue

            total_words = sum(_word_count(chunk) for chunk in chunks)

            if total_words <= 0:
                current_time = scene_end
                continue

            block_start = scene_start

            for chunk_index, chunk in enumerate(chunks):
                if chunk_index == len(chunks) - 1:
                    block_end = scene_end
                else:
                    proportion = _word_count(chunk) / total_words
                    block_duration = duration * proportion
                    block_end = block_start + block_duration

                blocks.append(
                    SubtitleBlock(
                        index=global_index,
                        text=chunk,
                        start_seconds=block_start,
                        end_seconds=block_end,
                    )
                )

                global_index += 1
                block_start = block_end

            current_time = scene_end

        return SubtitleGenerationResult(
            blocks=blocks,
            provider=self.provider_name,
            metadata={
                "mode": "word_weighted_chunks",
                "max_chars_per_line": request.max_chars_per_line,
                "max_lines": request.max_lines,
            },
        )


def _scene_duration_seconds(scene: dict) -> float:
    return float(scene.get("duration_seconds") or scene.get("duration") or 6.0)


def _split_text(
    text: str,
    max_chars: int,
) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    current_words: list[str] = []

    for word in words:
        candidate_words = [*current_words, word]
        candidate = " ".join(candidate_words)

        if len(candidate) <= max_chars:
            current_words = candidate_words
            continue

        if current_words:
            chunks.append(" ".join(current_words))

        current_words = [word]

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks


def _word_count(text: str) -> int:
    return len(text.split())
