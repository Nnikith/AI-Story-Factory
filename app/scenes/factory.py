from __future__ import annotations

from app.scenes.providers.base import ScenePlanner
from app.scenes.providers.heuristic import HeuristicScenePlanner


def create_scene_planner(provider_name: str) -> ScenePlanner:
    normalized = provider_name.strip().lower()

    if normalized in {"heuristic", "default", "simple"}:
        return HeuristicScenePlanner()

    raise ValueError(f"Unsupported scene planner: {provider_name}")
