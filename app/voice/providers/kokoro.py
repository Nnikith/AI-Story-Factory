from __future__ import annotations

from pathlib import Path

import soundfile as sf
from kokoro import KPipeline

from app.voice.models import VoiceGenerationRequest, VoiceGenerationResult
from app.voice.providers.base import VoiceProvider


class KokoroVoiceProvider(VoiceProvider):
    provider_name = "kokoro"

    def __init__(self, lang_code: str = "a") -> None:
        self.lang_code = lang_code
        self.pipeline = KPipeline(lang_code=lang_code)

    def generate(self, request: VoiceGenerationRequest) -> VoiceGenerationResult:
        request.output_path.parent.mkdir(parents=True, exist_ok=True)

        if request.output_path.exists() and not request.force:
            return VoiceGenerationResult(
                scene_id=request.scene_id,
                audio_path=request.output_path,
                provider=self.provider_name,
                duration_seconds=request.duration_seconds,
                cached=True,
            )

        audio_chunks = []
        generator = self.pipeline(
            request.text,
            voice=request.voice_name,
        )

        for _, _, audio in generator:
            audio_chunks.append(audio)

        if not audio_chunks:
            raise RuntimeError(f"Kokoro generated no audio for {request.scene_id}")

        output_path = Path(request.output_path)
        sf.write(
            output_path,
            audio_chunks[0] if len(audio_chunks) == 1 else _concat_audio(audio_chunks),
            request.sample_rate,
        )

        return VoiceGenerationResult(
            scene_id=request.scene_id,
            audio_path=output_path,
            provider=self.provider_name,
            duration_seconds=request.duration_seconds,
            cached=False,
            metadata={
                "lang_code": self.lang_code,
                "voice_name": request.voice_name,
                "sample_rate": request.sample_rate,
                "chunks": len(audio_chunks),
            },
        )


def _concat_audio(audio_chunks: list) -> object:
    import numpy as np

    return np.concatenate(audio_chunks)
