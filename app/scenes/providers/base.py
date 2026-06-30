from __future__ import annotations

from abc import ABC, abstractmethod

from app.scenes.models import ScenePlanningRequest, ScenePlanningResult


class ScenePlanner(ABC):
    provider_name: str

    @abstractmethod
    def plan(self, request: ScenePlanningRequest) -> ScenePlanningResult:
        """Create planned scenes from story text."""
