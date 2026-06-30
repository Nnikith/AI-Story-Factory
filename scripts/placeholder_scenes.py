from pathlib import Path
import json

out = Path("data/output")
out.mkdir(parents=True, exist_ok=True)

scenes = [
    {
        "scene_id": 1,
        "duration": 6,
        "narration": "A young hero wakes up in a strange fantasy world.",
        "image_prompt": "young hero waking up in a straw hut, fantasy anime style"
    },
    {
        "scene_id": 2,
        "duration": 6,
        "narration": "Around his neck hangs a mysterious pendant glowing with blue light.",
        "image_prompt": "mysterious blue pendant glowing, cinematic close up"
    },
    {
        "scene_id": 3,
        "duration": 6,
        "narration": "Outside, a small village waits under the shadow of a dangerous forest.",
        "image_prompt": "small fantasy village near dark forest, anime style"
    }
]

(out / "scenes.json").write_text(json.dumps(scenes, indent=2), encoding="utf-8")
print("Created data/output/scenes.json")
