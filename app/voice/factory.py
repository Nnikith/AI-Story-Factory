from __future__ import annotations

from app.voice.providers.base import VoiceProvider
from app.voice.providers.kokoro import KokoroVoiceProvider
from app.voice.providers.placeholder import PlaceholderVoiceProvider


def create_voice_provider(provider_name: str) -> VoiceProvider:
    normalized = provider_name.strip().lower()

    if normalized == "placeholder":
        return PlaceholderVoiceProvider()

    if normalized == "kokoro":
        return KokoroVoiceProvider()

    raise ValueError(f"Unsupported voice provider: {provider_name}")
