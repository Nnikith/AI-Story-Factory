from pathlib import Path
import json

out = Path("data/output")
sub_dir = out / "subtitles"
sub_dir.mkdir(parents=True, exist_ok=True)

scenes = json.loads((out / "scenes.json").read_text(encoding="utf-8"))

def fmt(ms):
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

current = 0
blocks = []
for i, scene in enumerate(scenes, 1):
    start = current
    end = current + scene["duration"] * 1000
    blocks.append(f"{i}\n{fmt(start)} --> {fmt(end)}\n{scene['narration']}\n")
    current = end

(sub_dir / "subtitles.srt").write_text("\n".join(blocks), encoding="utf-8")
print("Created subtitles.srt")
