from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict
from pathlib import Path
from typing import Any

from app.images.models import ImageGenerationRequest, ImageGenerationResult


class ImageCache:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.image_dir = cache_dir / "images"
        self.metadata_dir = cache_dir / "image_metadata"
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def build_key(
        self,
        request: ImageGenerationRequest,
        provider: str,
        extra: dict[str, Any] | None = None,
    ) -> str:
        payload = {
            "provider": provider,
            "prompt": request.prompt,
            "negative_prompt": request.negative_prompt,
            "width": request.width,
            "height": request.height,
            "seed": request.seed,
            "extra": extra or {},
        }

        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

    def image_path(self, cache_key: str) -> Path:
        return self.image_dir / f"{cache_key}.png"

    def metadata_path(self, cache_key: str) -> Path:
        return self.metadata_dir / f"{cache_key}.json"

    def has(self, cache_key: str) -> bool:
        return self.image_path(cache_key).exists() and self.metadata_path(cache_key).exists()

    def restore(
        self,
        cache_key: str,
        request: ImageGenerationRequest,
        provider: str,
    ) -> ImageGenerationResult:
        cached_image = self.image_path(cache_key)
        request.output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cached_image, request.output_path)

        return ImageGenerationResult(
            scene_id=request.scene_id,
            image_path=request.output_path,
            provider=provider,
            cached=True,
            seed=request.seed,
        )

    def save(
        self,
        cache_key: str,
        request: ImageGenerationRequest,
        result: ImageGenerationResult,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        cached_image = self.image_path(cache_key)
        cached_metadata = self.metadata_path(cache_key)

        shutil.copy2(result.image_path, cached_image)

        payload = {
            "cache_key": cache_key,
            "request": {
                "scene_id": request.scene_id,
                "prompt": request.prompt,
                "negative_prompt": request.negative_prompt,
                "width": request.width,
                "height": request.height,
                "seed": request.seed,
            },
            "result": {
                "scene_id": result.scene_id,
                "image_path": str(result.image_path),
                "provider": result.provider,
                "cached": result.cached,
                "seed": result.seed,
                "error": result.error,
            },
            "metadata": metadata or {},
        }

        with open(cached_metadata, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, ensure_ascii=False)
