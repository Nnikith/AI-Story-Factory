from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

from app.core.paths import CONFIG_DIR


class RenderConfig(BaseModel):
    aspect_ratio: str
    resolution: str
    fps: int
    codec: str = "libx264"
    crf: int = 23
    preset: str = "veryfast"


class SubtitleConfig(BaseModel):
    embed: bool
    font_name: str
    font_size: int
    position: str = "bottom_center"
    color: str = "white"
    outline_color: str = "black"
    max_lines: int = 3
    max_chars_per_line: int = 42
    provider: str = "placeholder"


class ImageConfig(BaseModel):
    provider: str
    style: str
    cache_enabled: bool

    width: int = 1024
    height: int = 576

    steps: int = 4
    guidance_scale: float = 0.0
    seed: int | None = 12345

    device: str = "cuda"
    dtype: str = "float16"

    model_name: str = "sdxl-turbo"
    model_path: str = "/home/nikith/Models/SDXL/sdxl-turbo"

    overwrite_existing: bool = False


class AudioConfig(BaseModel):
    voice_provider: str
    narration_volume: float = 1.0
    music_volume: float = 0.08
    cache_enabled: bool = True
    overwrite_existing: bool = False
    sample_rate: int = 24000
    voice_name: str = "af_heart"
    model_name: str = "kokoro"
    lang_code: str = "a"
    repo_id: str = "hexgrad/Kokoro-82M"


class Config(BaseModel):
    render: RenderConfig
    subtitles: SubtitleConfig
    images: ImageConfig
    audio: AudioConfig


def load_config(path: Path | None = None) -> Config:
    if path is None:
        path = CONFIG_DIR / "default.yaml"

    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return Config.model_validate(data)


settings = load_config()
