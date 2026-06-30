from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from app.voice.models import VoiceGenerationRequest, VoiceGenerationResult


class VoiceCache:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.audio_dir = cache_dir / "voice"
        self.metadata_dir = cache_dir / "voice_metadata"
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def build_key(
        self,
        request: VoiceGenerationRequest,
        provider: str,
        extra: dict[str, Any] | None = None,
    ) -> str:
        payload = {
            "provider": provider,
            "text": request.text,
            "duration_seconds": request.duration_seconds,
            "sample_rate": request.sample_rate,
            "voice_name": request.voice_name,
            "extra": extra or {},
        }

        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

    def audio_path(self, cache_key: str) -> Path:
        return self.audio_dir / f"{cache_key}.wav"

    def metadata_path(self, cache_key: str) -> Path:
        return self.metadata_dir / f"{cache_key}.json"

    def has(self, cache_key: str) -> bool:
        return self.audio_path(cache_key).exists() and self.metadata_path(cache_key).exists()

    def restore(
        self,
        cache_key: str,
        request: VoiceGenerationRequest,
        provider: str,
    ) -> VoiceGenerationResult:
        cached_audio = self.audio_path(cache_key)
        request.output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cached_audio, request.output_path)

        return VoiceGenerationResult(
            scene_id=request.scene_id,
            audio_path=request.output_path,
            provider=provider,
            duration_seconds=request.duration_seconds,
            cached=True,
        )

    def save(
        self,
        cache_key: str,
        request: VoiceGenerationRequest,
        result: VoiceGenerationResult,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        cached_audio = self.audio_path(cache_key)
        cached_metadata = self.metadata_path(cache_key)

        shutil.copy2(result.audio_path, cached_audio)

        payload = {
            "cache_key": cache_key,
            "request": {
                "scene_id": request.scene_id,
                "text": request.text,
                "output_path": str(request.output_path),
                "duration_seconds": request.duration_seconds,
                "sample_rate": request.sample_rate,
                "voice_name": request.voice_name,
            },
            "result": {
                "scene_id": result.scene_id,
                "audio_path": str(result.audio_path),
                "provider": result.provider,
                "duration_seconds": result.duration_seconds,
                "cached": result.cached,
                "error": result.error,
            },
            "metadata": metadata or {},
        }

        with open(cached_metadata, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, ensure_ascii=False)
