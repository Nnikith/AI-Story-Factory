from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from app.images.models import ImageGenerationRequest, ImageGenerationResult
from app.images.providers.base import ImageProvider


class PlaceholderImageProvider(ImageProvider):
    provider_name = "placeholder"

    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        request.output_path.parent.mkdir(parents=True, exist_ok=True)

        if request.output_path.exists() and not request.force:
            return ImageGenerationResult(
                scene_id=request.scene_id,
                image_path=request.output_path,
                provider=self.provider_name,
                cached=True,
                seed=request.seed,
            )

        image = Image.new("RGB", (request.width, request.height), color=(24, 24, 32))
        draw = ImageDraw.Draw(image)

        title = request.scene_id.replace("_", " ").title()
        text = f"{title}\n\n{request.prompt[:180]}"

        try:
            font = ImageFont.truetype("DejaVuSans.ttf", 42)
        except OSError:
            font = ImageFont.load_default()

        draw.multiline_text(
            (80, 80),
            text,
            fill=(255, 255, 255),
            font=font,
            spacing=16,
        )

        image.save(request.output_path)

        return ImageGenerationResult(
            scene_id=request.scene_id,
            image_path=request.output_path,
            provider=self.provider_name,
            cached=False,
            seed=request.seed,
        )
