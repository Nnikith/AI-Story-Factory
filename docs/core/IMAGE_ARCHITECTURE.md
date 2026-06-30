# Image Architecture

The image subsystem is provider-based.

## Package

```text
app/images/
  cache.py
  factory.py
  models.py
  providers/
    base.py
    placeholder.py
    local_ai.py
```

## Responsibilities

- Read scene image prompts from `timeline.json`.
- Generate images using the configured provider.
- Cache expensive outputs.
- Update each scene with `image_path`, status, and metadata.

## Providers

Current providers:

- `placeholder`
- `local_ai`

## Cache

Image cache keys include prompt, negative prompt, resolution, seed, provider, and model settings.

## Rule

Stage 2 consumes timeline data and must not modify narration, scene order, or downstream assets.
