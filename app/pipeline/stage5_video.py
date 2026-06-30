from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from app.core.config import settings
from app.core.timeline import Timeline


TIMELINE_PATH = Path("data/output/timeline.json")
AUDIO_PATH = Path("data/output/audio/narration.wav")
SUBTITLE_PATH = Path("data/output/subtitles/subtitles.srt")
VIDEO_PATH = Path("data/output/videos/demo.mp4")


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

        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=True)

    for scene in timeline.scenes:
        scene.setdefault("status", {})["render"] = "done"

    timeline.data.setdefault("outputs", {})
    timeline.data["outputs"]["video"] = str(VIDEO_PATH)

    timeline.save(TIMELINE_PATH)

    print(f"Created video: {VIDEO_PATH}")


if __name__ == "__main__":
    run()
