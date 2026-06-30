# Architecture

## High-Level Pipeline

```text
Story Input
    ↓
Story Analyzer
    ↓
Narration Generator
    ↓
Scene Splitter
    ↓
Voice Generator
    ↓
Subtitle Builder
    ↓
Image Generator
    ↓
Video Renderer
    ↓
Thumbnail Generator
    ↓
Metadata Generator
    ↓
Upload / Export
```

## MVP Pipeline

```text
story.txt
    ↓
scenes.json
    ↓
placeholder images
    ↓
narration audio
    ↓
subtitles.srt
    ↓
demo.mp4
```

## Core Design Principle

Each module should be replaceable.

For example:

- Placeholder images can later become SDXL images.
- Simple voice can later become ElevenLabs or local TTS.
- Basic subtitles can later become animated subtitles.
- Landscape render can later support vertical Shorts.

## Main Modules

### `app/script`

Responsible for story cleanup and narration generation.

### `app/scenes`

Responsible for splitting narration into scenes.

### `app/images`

Responsible for generating or retrieving images.

### `app/voice`

Responsible for creating voice narration.

### `app/subtitles`

Responsible for subtitles, timestamps, and styling.

### `app/renderer`

Responsible for combining images, audio, subtitles, music, and motion into video.

### `app/metadata`

Responsible for title, description, tags, and thumbnail prompts.

## Data Flow

```text
data/input/story.txt
data/output/scenes.json
data/output/images/
data/output/audio/
data/output/subtitles/
data/output/videos/
```

## Rendering Targets

Initial target:

```text
1920x1080, 30 FPS, landscape
```

Future targets:

```text
1080x1920, vertical
1080x1080, square
```
