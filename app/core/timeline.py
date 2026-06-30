from __future__ import annotations

import json

from pathlib import Path

from app.core.models import Scene


class Timeline:

    def __init__(self, data: dict):

        self.data = data

    @classmethod
    def load(cls, path: Path):

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return cls(data)

    def save(self, path: Path):

        with open(path, "w", encoding="utf-8") as file:

            json.dump(
                self.data,
                file,
                indent=2,
                ensure_ascii=False,
            )

    @property
    def scenes(self):

        return self.data["scenes"]