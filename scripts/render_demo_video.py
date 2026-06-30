from pathlib import Path
import json
import subprocess
import tempfile

ROOT = Path(".")
OUT = ROOT / "data" / "output"
IMG_DIR = OUT / "images"
AUDIO = OUT / "audio" / "narration.wav"
SUBS = OUT / "subtitles" / "subtitles.srt"
VIDEO_DIR = OUT / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
FINAL = VIDEO_DIR / "demo.mp4"

scenes_path = OUT / "scenes.json"
if not scenes_path.exists():
    raise SystemExit("Missing data/output/scenes.json. Run make scenes first.")

scenes = json.loads(scenes_path.read_text(encoding="utf-8"))

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    concat_file = tmp / "images.txt"
    lines = []
    for scene in scenes:
        image = IMG_DIR / f"scene_{scene['scene_id']:03d}.png"
        duration = float(scene.get("duration", 6))
        if not image.exists():
            raise SystemExit(f"Missing image: {image}")
        lines.append(f"file '{image.resolve()}'")
        lines.append(f"duration {duration}")
    # repeat final image for ffmpeg concat demuxer
    last = IMG_DIR / f"scene_{scenes[-1]['scene_id']:03d}.png"
    lines.append(f"file '{last.resolve()}'")
    concat_file.write_text("\n".join(lines), encoding="utf-8")

    subtitle_filter = ""
    if SUBS.exists():
        # force_style gives readable embedded subtitles
        subtitle_filter = (
            f"subtitles='{SUBS.resolve()}':"
            "force_style='FontName=Arial,FontSize=36,"
            "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
            "BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=70'"
        )

    vf = "scale=1920:1080,format=yuv420p"
    if subtitle_filter:
        vf = f"{vf},{subtitle_filter}"

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
    ]

    if AUDIO.exists():
        cmd += ["-i", str(AUDIO), "-shortest"]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-shortest"]

    cmd += [
        "-vf", vf,
        "-r", "30",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        str(FINAL),
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

print(f"Created {FINAL}")
