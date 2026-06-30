from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

from app.core.paths import CONFIG_DIR


class RenderConfig(BaseModel):
    aspect_ratio: str
    resolution: str
    fps: int


class SubtitleConfig(BaseModel):
    embed: bool
    font_name: str
    font_size: int


class ImageConfig(BaseModel):
    provider: str
    style: str
    cache_enabled: bool


class AudioConfig(BaseModel):
    voice_provider: str


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