# Milestones

## Milestone 0 — Project Setup

Status: Not started

Deliverables:

- Git repository
- WSL2 development environment
- VS Code Remote WSL setup
- Makefile
- Project folders
- First commit

Acceptance test:

```bash
make check
```

## Milestone 1 — Text to Scene JSON

Status: Not started

Input:

```text
data/input/story.txt
```

Output:

```text
data/output/scenes.json
```

Acceptance test:

```bash
make scenes
```

## Milestone 2 — Placeholder Images

Status: Not started

Output:

```text
data/output/images/scene_001.png
```

Acceptance test:

```bash
make images
```

## Milestone 3 — Voice

Status: Not started

Output:

```text
data/output/audio/narration.wav
```

Acceptance test:

```bash
make voice
```

## Milestone 4 — Subtitles

Status: Not started

Output:

```text
data/output/subtitles/subtitles.srt
```

Acceptance test:

```bash
make subtitles
```

## Milestone 5 — MP4 Render

Status: Not started

Output:

```text
data/output/videos/demo.mp4
```

Acceptance test:

```bash
make render
```

## Milestone 6 — Local AI Images

Status: Later

Replace placeholders with AI-generated images.

## Milestone 7 — Thumbnail and Metadata

Status: Later

Generate:

- Thumbnail
- Title
- Description
- Tags

## Milestone 8 — Batch Mode

Status: Later

Generate multiple videos in a queue.
