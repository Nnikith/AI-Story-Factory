from __future__ import annotations

from pydantic import BaseModel


class CameraMotion(BaseModel):
    type: str
    strength: float


class SceneStatus(BaseModel):
    script: str
    image: str
    voice: str
    subtitle: str
    render: str


class Scene(BaseModel):

    scene_id: str

    order: int

    duration_seconds: float

    narration: str

    image_prompt: str

    image_path: str

    audio_path: str

    subtitle_text: str

    subtitle_start: float

    subtitle_end: float

    camera: CameraMotion

    status: SceneStatus