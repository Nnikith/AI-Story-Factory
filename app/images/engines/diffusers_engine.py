from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import AutoPipelineForText2Image

from app.core.config import settings
from app.images.engines.base import ImageEngine
from app.images.models import ImageGenerationRequest, ImageGenerationResult


class DiffusersEngine(ImageEngine):
    engine_name = "diffusers"

    def __init__(self) -> None:
        self._pipeline = None
        self._load_time_seconds: float | None = None

    def _torch_dtype(self) -> torch.dtype:
        dtype = settings.images.dtype.lower()

        if dtype == "float16":
            return torch.float16

        if dtype == "bfloat16":
            return torch.bfloat16

        return torch.float32

    def _load_pipeline(self):
        if self._pipeline is not None:
            return self._pipeline

        started_at = time.perf_counter()

        pipeline = AutoPipelineForText2Image.from_pretrained(
            settings.images.model_path,
            torch_dtype=self._torch_dtype(),
            variant="fp16" if settings.images.dtype == "float16" else None,
        )

        pipeline = pipeline.to(settings.images.device)

        if hasattr(pipeline, "enable_attention_slicing"):
            pipeline.enable_attention_slicing()

        self._pipeline = pipeline
        self._load_time_seconds = time.perf_counter() - started_at

        return self._pipeline

    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        total_started_at = time.perf_counter()

        request.output_path.parent.mkdir(parents=True, exist_ok=True)

        pipeline = self._load_pipeline()

        generator = None
        if request.seed is not None:
            generator = torch.Generator(device=settings.images.device).manual_seed(
                request.seed
            )

        generation_started_at = time.perf_counter()

        image = pipeline(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt or None,
            width=request.width,
            height=request.height,
            num_inference_steps=settings.images.steps,
            guidance_scale=settings.images.guidance_scale,
            generator=generator,
        ).images[0]

        generation_time = time.perf_counter() - generation_started_at
        total_time = time.perf_counter() - total_started_at

        image.save(request.output_path)

        return ImageGenerationResult(
            scene_id=request.scene_id,
            image_path=Path(request.output_path),
            provider="local_ai",
            cached=False,
            seed=request.seed,
            metadata={
                "engine": self.engine_name,
                "model_name": settings.images.model_name,
                "model_path": settings.images.model_path,
                "steps": settings.images.steps,
                "guidance_scale": settings.images.guidance_scale,
                "dtype": settings.images.dtype,
                "device": settings.images.device,
                "load_time_seconds": self._load_time_seconds,
                "generation_time_seconds": generation_time,
                "total_time_seconds": total_time,
            },
        )
