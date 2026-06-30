# Timeline Schema

## Purpose

`timeline.json` is the central contract of AI Story Factory.

Every pipeline stage reads the timeline, updates its own fields, and writes the timeline back.

```text
story.txt
  ↓
timeline.json
  ↓
images
  ↓
voice
  ↓
subtitles
  ↓
video
```

## Core Rule

The renderer should only need `timeline.json` plus referenced asset files.

## File Location

Default path:

```text
data/output/timeline.json
```

## Top-Level Structure

```json
{
  "project": {},
  "source": {},
  "settings": {},
  "characters": [],
  "scenes": [],
  "assets": {},
  "outputs": {},
  "run": {}
}
```

## Required Fields

### `project`

```json
{
  "name": "AI Story Factory Demo",
  "version": "0.0.1",
  "created_at": "2026-06-30T00:00:00Z"
}
```

### `source`

```json
{
  "type": "story_text",
  "path": "data/input/story.txt",
  "title": "Demo Story",
  "language": "en"
}
```

### `settings`

```json
{
  "aspect_ratio": "16:9",
  "resolution": "1920x1080",
  "fps": 30,
  "subtitle_style": "default",
  "image_style": "cinematic anime fantasy",
  "voice": "default"
}
```

### `characters`

```json
[
  {
    "character_id": "hero",
    "name": "Hero",
    "description": "Young fantasy hero with black hair and simple armor.",
    "visual_prompt": "young male fantasy hero, black hair, simple armor",
    "negative_prompt": "different face, old man, modern clothing"
  }
]
```

### `scenes`

Each scene represents one visual/narration unit.

```json
{
  "scene_id": "scene_001",
  "order": 1,
  "duration_seconds": 6.0,
  "narration": "A young hero wakes up in a strange fantasy world.",
  "image_prompt": "young hero waking up in a straw hut, cinematic anime style",
  "negative_prompt": "low quality, blurry, extra fingers",
  "characters": ["hero"],
  "location": "straw hut",
  "mood": "mysterious",
  "image_path": "data/output/images/scene_001.png",
  "audio_path": "data/output/audio/scene_001.wav",
  "subtitle_text": "A young hero wakes up\nin a strange fantasy world.",
  "subtitle_start": 0.0,
  "subtitle_end": 6.0,
  "camera": {
    "type": "slow_zoom_in",
    "strength": 0.08
  },
  "status": {
    "script": "done",
    "image": "pending",
    "voice": "pending",
    "subtitle": "pending",
    "render": "pending"
  }
}
```

## Scene Status Values

Allowed status values:

```text
pending
running
done
failed
skipped
```

## Asset Paths

All paths should be relative to the project root when possible.

Example:

```json
{
  "assets": {
    "music": "assets/music/default_loop.mp3",
    "font": "assets/fonts/default.ttf"
  }
}
```

## Outputs

```json
{
  "outputs": {
    "video": "data/output/videos/demo.mp4",
    "subtitles": "data/output/subtitles/subtitles.srt",
    "metadata": "data/output/metadata/youtube.json"
  }
}
```

## Run Metadata

```json
{
  "run": {
    "run_id": "20260630_120000",
    "started_at": "2026-06-30T12:00:00Z",
    "completed_at": null,
    "errors": [],
    "warnings": []
  }
}
```

## Design Decisions

- The timeline is append/update based.
- Stages should not delete unrelated fields.
- Stages should be resumable.
- Each scene should be independently processable.
- Asset generation should be cacheable by prompt hash.
- Renderer should not call LLMs or image models directly.

## Future Extensions

Possible future fields:

```json
{
  "shot_type": "close_up",
  "transition": "crossfade",
  "music_cue": "battle",
  "sound_effects": [],
  "thumbnail_candidate": true,
  "shorts_candidate": true
}
```
