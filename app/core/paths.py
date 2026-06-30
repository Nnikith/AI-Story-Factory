from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

APP_DIR = PROJECT_ROOT / "app"

CONFIG_DIR = PROJECT_ROOT / "configs"

DATA_DIR = PROJECT_ROOT / "data"

INPUT_DIR = DATA_DIR / "input"

OUTPUT_DIR = DATA_DIR / "output"

CACHE_DIR = DATA_DIR / "cache"

LOG_DIR = DATA_DIR / "logs"

ASSETS_DIR = PROJECT_ROOT / "assets"

MODELS_DIR = Path.home() / "Models"


def ensure_directories() -> None:
    directories = [
        INPUT_DIR,
        OUTPUT_DIR,
        CACHE_DIR,
        LOG_DIR,
        OUTPUT_DIR / "images",
        OUTPUT_DIR / "audio",
        OUTPUT_DIR / "videos",
        OUTPUT_DIR / "subtitles",
        OUTPUT_DIR / "metadata",
        OUTPUT_DIR / "scenes",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)