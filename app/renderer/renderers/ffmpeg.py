from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.renderer.models import RenderRequest, RenderResult
from app.renderer.renderers.base import VideoRenderer

logger = get_logger("ffmpeg_renderer")


class FfmpegRenderer(VideoRenderer):
    renderer_name = "ffmpeg"

    def render(self, request: RenderRequest) -> RenderResult:
        audio_path = _audio_input_path(request.timeline_data)

        request.output_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmp_dir:
            concat_file = Path(tmp_dir) / "images.txt"
            lines: list[str] = []

            scenes = request.timeline_data["scenes"]

            for scene in scenes:
                image_path = Path(scene["image_path"])
                duration = _scene_duration_seconds(scene)

                if not image_path.exists():
                    raise FileNotFoundError(f"Missing image: {image_path}")

                lines.append(f"file '{image_path.resolve()}'")
                lines.append(f"duration {duration}")

            last_image = Path(scenes[-1]["image_path"])
            lines.append(f"file '{last_image.resolve()}'")

            concat_file.write_text("\n".join(lines), encoding="utf-8")

            vf = f"scale={request.resolution.replace('x', ':')},format=yuv420p"

            subtitle_filter = _subtitle_filter(request.subtitle_path)
            if subtitle_filter:
                vf = f"{vf},{subtitle_filter}"

            cmd = [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
            ]

            if audio_path:
                cmd += ["-i", str(audio_path), "-shortest"]
            else:
                logger.warning("Missing narration audio, using silent fallback")
                cmd += [
                    "-f",
                    "lavfi",
                    "-i",
                    "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-shortest",
                ]

            cmd += [
                "-vf",
                vf,
                "-r",
                str(request.fps),
                "-c:v",
                request.codec,
                "-preset",
                request.preset,
                "-crf",
                str(request.crf),
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                str(request.output_path),
            ]

            logger.info("Running FFmpeg command: %s", " ".join(cmd))

            try:
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except subprocess.CalledProcessError as exc:
                logger.error("FFmpeg failed with exit code %s", exc.returncode)
                if exc.stdout:
                    logger.error("FFmpeg stdout: %s", exc.stdout)
                if exc.stderr:
                    logger.error("FFmpeg stderr: %s", exc.stderr)
                raise

            if result.stdout:
                logger.debug("FFmpeg stdout: %s", result.stdout)

            if result.stderr:
                logger.debug("FFmpeg stderr: %s", result.stderr)

        return RenderResult(
            video_path=request.output_path,
            renderer=self.renderer_name,
            metadata={
                "resolution": request.resolution,
                "fps": request.fps,
                "codec": request.codec,
                "crf": request.crf,
                "preset": request.preset,
            },
        )


def _audio_input_path(timeline_data: dict) -> Path | None:
    scenes = timeline_data.get("scenes", [])
    if not scenes:
        return None

    audio = scenes[0].get("audio_path")
    if not audio:
        return None

    path = Path(audio)
    return path if path.exists() else None


def _scene_duration_seconds(scene: dict) -> float:
    return float(scene.get("duration_seconds") or scene.get("duration") or 6.0)


def _subtitle_filter(subtitle_path: Path) -> str:
    if not subtitle_path.exists():
        return ""

    subtitle = settings.subtitles

    force_style = ",".join(
        [
            f"FontName={subtitle.font_name}",
            f"FontSize={subtitle.font_size}",
            "PrimaryColour=&H00FFFFFF",
            "OutlineColour=&H00000000",
            "BorderStyle=1",
            "Outline=2",
            "Shadow=1",
            "Alignment=2",
            "MarginV=70",
        ]
    )

    return f"subtitles='{subtitle_path.resolve()}':force_style='{force_style}'"
