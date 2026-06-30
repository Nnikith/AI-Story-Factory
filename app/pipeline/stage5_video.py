from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger
from app.core.timeline import Timeline
import time

TIMELINE_PATH = Path("data/output/timeline.json")
AUDIO_PATH = Path("data/output/audio/narration.wav")
SUBTITLE_PATH = Path("data/output/subtitles/subtitles.srt")
VIDEO_PATH = Path("data/output/videos/demo.mp4")

logger = get_logger("stage5_video")


def _scene_duration_seconds(scene: dict) -> float:
    return float(scene.get("duration_seconds") or scene.get("duration") or 6.0)


def _subtitle_filter() -> str:
    if not SUBTITLE_PATH.exists():
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

    return f"subtitles='{SUBTITLE_PATH.resolve()}':force_style='{force_style}'"


def run() -> None:
    logger.info("Starting Stage 5 video render")
    started_at = time.perf_counter()

    timeline = Timeline.load(TIMELINE_PATH)
    VIDEO_PATH.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        concat_file = Path(tmp_dir) / "images.txt"
        lines: list[str] = []

        for scene in timeline.scenes:
            image_path = Path(scene["image_path"])
            duration = _scene_duration_seconds(scene)

            if not image_path.exists():
                raise FileNotFoundError(f"Missing image: {image_path}")

            lines.append(f"file '{image_path.resolve()}'")
            lines.append(f"duration {duration}")

        last_image = Path(timeline.scenes[-1]["image_path"])
        lines.append(f"file '{last_image.resolve()}'")

        concat_file.write_text("\n".join(lines), encoding="utf-8")

        vf = f"scale={settings.render.resolution.replace('x', ':')},format=yuv420p"

        subtitle_filter = _subtitle_filter()
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

        if AUDIO_PATH.exists():
            cmd += ["-i", str(AUDIO_PATH), "-shortest"]
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
            str(settings.render.fps),
            "-c:v",
            settings.render.codec,
            "-preset",
            settings.render.preset,
            "-crf",
            str(settings.render.crf),
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            str(VIDEO_PATH),
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
        

        if result.stderr:
            logger.debug(result.stderr)
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            logger.error("FFmpeg failed")
            logger.error(exc.stderr)
            raise

    for scene in timeline.scenes:
        scene.setdefault("status", {})["render"] = "done"

    timeline.data.setdefault("outputs", {})
    timeline.data["outputs"]["video"] = str(VIDEO_PATH)

    timeline.save(TIMELINE_PATH)

    elapsed = time.perf_counter() - started_at
    logger.info("Stage 5 complete: created video path=%s elapsed=%.2fs", VIDEO_PATH, elapsed)


if __name__ == "__main__":
    run()
