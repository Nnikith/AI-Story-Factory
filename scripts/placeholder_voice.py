from pathlib import Path
from pydub import AudioSegment
import json

out = Path("data/output")
audio_dir = out / "audio"
audio_dir.mkdir(parents=True, exist_ok=True)

scenes = json.loads((out / "scenes.json").read_text(encoding="utf-8"))
total_ms = sum(scene["duration"] for scene in scenes) * 1000

silent = AudioSegment.silent(duration=total_ms)
silent.export(audio_dir / "narration.wav", format="wav")

print("Created placeholder silent narration")
