from __future__ import annotations

from app.motion.models import MotionRequest, MotionResult
from app.motion.providers.base import MotionProvider


class NoMotionProvider(MotionProvider):
    provider_name = "none"

    def build_filter(self, request: MotionRequest) -> MotionResult:
        scene_id = str(request.scene.get("scene_id") or request.scene.get("id"))

        return MotionResult(
            scene_id=scene_id,
            provider=self.provider_name,
            filter_chain="",
            metadata={
                "motion": "none",
            },
        )
