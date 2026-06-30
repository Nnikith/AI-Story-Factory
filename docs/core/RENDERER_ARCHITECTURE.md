# Renderer Architecture

The renderer subsystem combines timeline assets into the final video.

## Packages

```text
app/renderer/
  factory.py
  models.py
  renderers/
    base.py
    ffmpeg.py

app/motion/
  factory.py
  models.py
  providers/
    base.py
    none.py
    ken_burns.py
```

## Responsibilities

Renderer:

- read timeline asset paths
- create scene clips
- combine scene clips
- burn subtitles
- attach audio
- export MP4

Motion provider:

- read scene camera metadata
- generate FFmpeg filter chains
- write motion metadata back to the timeline

## Current Renderer

- `ffmpeg`

## Current Motion Providers

- `none`
- `ken_burns`
