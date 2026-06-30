from __future__ import annotations

from app.motion.providers.base import MotionProvider
from app.motion.providers.ken_burns import KenBurnsMotionProvider
from app.motion.providers.none import NoMotionProvider


def create_motion_provider(provider_name: str) -> MotionProvider:
    normalized = provider_name.strip().lower()

    if normalized in {"none", "disabled", "off"}:
        return NoMotionProvider()

    if normalized in {"ken_burns", "ken-burns", "kenburns"}:
        return KenBurnsMotionProvider()

    raise ValueError(f"Unsupported motion provider: {provider_name}")
