# Configuration Guide

## Purpose

Configuration controls project behavior without changing code.

## Main Config File

Default config:

```text
configs/default.yaml
```

Future overrides:

```text
configs/development.yaml
configs/production.yaml
configs/local.yaml
```

## Configuration Priority

Highest priority wins:

```text
CLI argument
.env variable
configs/local.yaml
configs/development.yaml
configs/default.yaml
hardcoded fallback
```

## Required Config Sections

```yaml
project:
  name: AI Story Factory
  version: 0.0.1

paths:
  input_dir: data/input
  output_dir: data/output
  cache_dir: data/cache
  model_root: /home/nikith/Models

render:
  aspect_ratio: "16:9"
  resolution: "1920x1080"
  fps: 30

subtitles:
  embed: true
  font_name: "Arial"
  font_size: 54

audio:
  voice_provider: "placeholder"

images:
  provider: "placeholder"
  style: "cinematic anime fantasy"
```

## Environment Variables

Stored in `.env`.

Never commit `.env`.

Use `.env.example` for safe examples.

Common variables:

```text
OPENAI_API_KEY=
ELEVENLABS_API_KEY=
MODEL_ROOT=/home/nikith/Models
OUTPUT_ROOT=./data/output
CACHE_ROOT=./data/cache
```

## Paths

Code should not hardcode paths.

Bad:

```python
output = "/home/nikith/projects/AI-Story-Factory/data/output"
```

Good:

```python
output = settings.paths.output_dir
```

## Models

Large models should not be stored in the repo.

Preferred location:

```text
/home/nikith/Models
```

Examples:

```text
/home/nikith/Models/SDXL
/home/nikith/Models/Whisper
/home/nikith/Models/TTS
```

## Output Settings

Landscape default:

```yaml
render:
  aspect_ratio: "16:9"
  resolution: "1920x1080"
  fps: 30
```

Future vertical output:

```yaml
render:
  aspect_ratio: "9:16"
  resolution: "1080x1920"
  fps: 30
```

## Subtitle Settings

Recommended defaults:

```yaml
subtitles:
  embed: true
  font_name: "Arial"
  font_size: 54
  color: "white"
  outline_color: "black"
  max_lines: 3
  max_chars_per_line: 42
```

## Cache Settings

```yaml
cache:
  enabled: true
  prompt_hashing: true
  skip_existing: true
```

## Local Overrides

`configs/local.yaml` may contain machine-specific values.

It should be gitignored if it includes private paths or secrets.

## Rule

If a value might change between machines, videos, models, or formats, put it in config.
