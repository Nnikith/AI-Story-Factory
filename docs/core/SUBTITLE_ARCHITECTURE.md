# Subtitle Architecture

The subtitle subsystem is provider-based.

## Package

```text
app/subtitles/
  factory.py
  models.py
  providers/
    base.py
    placeholder.py
```

## Responsibilities

- Create readable subtitle chunks.
- Assign deterministic timing.
- Write SRT.
- Store subtitle metadata in the timeline.

## Current Behavior

The placeholder provider now supports:

- readable chunking
- word-weighted timing
- balanced multiline formatting

## Timeline Fields

Each scene may contain:

```json
"subtitles": [
  {
    "index": 1,
    "text": "A young hero wakes up\nin a strange fantasy",
    "start_seconds": 0.0,
    "end_seconds": 2.06
  }
]
```
