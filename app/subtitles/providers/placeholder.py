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

            block_duration = duration / len(chunks)

            for chunk_index, chunk in enumerate(chunks):
                start = scene_start + (chunk_index * block_duration)

                if chunk_index == len(chunks) - 1:
                    end = scene_end
                else:
                    end = scene_start + ((chunk_index + 1) * block_duration)

                blocks.append(
                    SubtitleBlock(
                        index=global_index,
                        text=chunk,
                        start_seconds=start,
                        end_seconds=end,
                    )
                )
                global_index += 1

            current_time = scene_end

        return SubtitleGenerationResult(
            blocks=blocks,
            provider=self.provider_name,
            metadata={
                "mode": "readable_chunks",
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
