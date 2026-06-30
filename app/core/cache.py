from __future__ import annotations

import hashlib


def prompt_hash(prompt: str) -> str:

    return hashlib.sha256(
        prompt.encode("utf-8")
    ).hexdigest()


def is_cached(cache: dict, prompt: str) -> bool:

    return prompt_hash(prompt) in cache