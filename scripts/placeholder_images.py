from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

out = Path("data/output")
img_dir = out / "images"
img_dir.mkdir(parents=True, exist_ok=True)

scenes = json.loads((out / "scenes.json").read_text(encoding="utf-8"))

for scene in scenes:
    img = Image.new("RGB", (1920, 1080), (30, 30, 35))
    draw = ImageDraw.Draw(img)
    text = f"Scene {scene['scene_id']}\n{scene['image_prompt']}"
    draw.multiline_text((120, 420), text, fill=(255, 255, 255), spacing=20)
    img.save(img_dir / f"scene_{scene['scene_id']:03d}.png")

print("Created placeholder images")
