from __future__ import annotations

from app.motion.models import MotionRequest, MotionResult
from app.motion.providers.base import MotionProvider


class KenBurnsMotionProvider(MotionProvider):
    provider_name = "ken_burns"

    def build_filter(self, request: MotionRequest) -> MotionResult:
        scene_id = str(request.scene.get("scene_id") or request.scene.get("id"))
        camera = request.scene.get("camera") or {}

        motion_type = str(camera.get("type") or "slow_zoom_in")
        strength = float(camera.get("strength") or 0.08)

        filter_chain = _build_zoompan_filter(
            motion_type=motion_type,
            strength=strength,
            width=request.width,
            height=request.height,
            fps=request.fps,
            duration_seconds=_scene_duration_seconds(request.scene),
        )

        return MotionResult(
            scene_id=scene_id,
            provider=self.provider_name,
            filter_chain=filter_chain,
            metadata={
                "motion_type": motion_type,
                "strength": strength,
                "width": request.width,
                "height": request.height,
                "fps": request.fps,
            },
        )


def _scene_duration_seconds(scene: dict) -> float:
    return float(scene.get("duration_seconds") or scene.get("duration") or 6.0)


def _build_zoompan_filter(
    motion_type: str,
    strength: float,
    width: int,
    height: int,
    fps: int,
    duration_seconds: float,
) -> str:
    total_frames = max(1, int(duration_seconds * fps))
    max_zoom = 1.0 + max(0.0, strength)

    if motion_type == "slow_zoom_out":
        zoom_expr = f"if(eq(on,0),{max_zoom},zoom-(({max_zoom}-1)/{total_frames}))"
    else:
        zoom_expr = f"min(zoom+(({max_zoom}-1)/{total_frames}),{max_zoom})"

    return (
        "zoompan="
        f"z='{zoom_expr}':"
        "x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)':"
        f"d={total_frames}:"
        f"s={width}x{height}:"
        f"fps={fps}"
    )
