from __future__ import annotations

from pydub import AudioSegment

from app.voice.models import VoiceGenerationRequest, VoiceGenerationResult
from app.voice.providers.base import VoiceProvider


class PlaceholderVoiceProvider(VoiceProvider):
    provider_name = "placeholder"

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

        duration_ms = int(request.duration_seconds * 1000)
        audio = AudioSegment.silent(duration=duration_ms)
        audio.export(request.output_path, format="wav")

        return VoiceGenerationResult(
            scene_id=request.scene_id,
            audio_path=request.output_path,
            provider=self.provider_name,
            duration_seconds=request.duration_seconds,
            cached=False,
            metadata={
                "sample_rate": request.sample_rate,
                "voice_name": request.voice_name,
            },
        )
