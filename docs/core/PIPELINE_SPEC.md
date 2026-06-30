# Pipeline Specification

## Purpose

This document defines how each pipeline stage works and what each stage consumes and produces.

## Main Pipeline

```text
Stage 1: Story
Stage 2: Images
Stage 3: Voice
Stage 4: Subtitles
Stage 5: Video
Stage 6: Metadata
```

## Golden Rule

Every stage must be independently runnable and resumable.

Example:

```bash
make stage1
make stage2
make stage3
make stage4
make stage5
```

## Stage 1 — Story to Timeline

Input:

```text
data/input/story.txt
```

Output:

```text
data/output/timeline.json
```

Responsibilities:

- Read story input.
- Clean text.
- Generate narration.
- Split narration into scenes.
- Create initial image prompts.
- Create scene durations.
- Create initial timeline.

Does not:

- Generate images.
- Generate voice.
- Generate subtitles.
- Render video.

## Stage 2 — Image Generation

Input:

```text
data/output/timeline.json
```

Output:

```text
data/output/images/
data/output/timeline.json
```

Responsibilities:

- Read scene image prompts.
- Generate or reuse cached images.
- Update each scene with `image_path`.
- Mark image status.

Does not:

- Change narration.
- Change scene order.
- Render video.

## Stage 3 — Voice Generation

Input:

```text
data/output/timeline.json
```

Output:

```text
data/output/audio/
data/output/timeline.json
```

Responsibilities:

- Generate narration audio.
- Create scene-level or full narration audio.
- Update audio paths.
- Estimate or store duration.

Does not:

- Generate images.
- Create final subtitles unless word timing is available.

## Stage 4 — Subtitles

Input:

```text
data/output/timeline.json`
```

Output:

```text
data/output/subtitles/subtitles.srt
data/output/timeline.json
```

Responsibilities:

- Create readable subtitle chunks.
- Align subtitles with audio/timeline.
- Write SRT.
- Store subtitle text and timestamps in timeline.

## Stage 5 — Video Renderer

Input:

```text
data/output/timeline.json
```

Output:

```text
data/output/videos/demo.mp4
```

Responsibilities:

- Read timeline.
- Load images.
- Load audio.
- Burn subtitles into video.
- Add camera motion.
- Add transitions.
- Export MP4.

Does not:

- Modify story.
- Generate AI images.
- Generate voice.

## Stage 6 — Metadata

Input:

```text
data/output/timeline.json
```

Output:

```text
data/output/metadata/youtube.json
```

Responsibilities:

- Generate title.
- Generate description.
- Generate tags.
- Generate chapter timestamps.
- Generate thumbnail prompt.

## Required Make Targets

```bash
make stage1
make stage2
make stage3
make stage4
make stage5
make demo
make smoke
make doctor
```

## Resume Behavior

Each stage should skip completed work unless forced.

Example:

```bash
make stage2
```

If `scene_001.png` already exists and the prompt hash has not changed, Stage 2 should skip regeneration.

## Force Behavior

Future command:

```bash
make stage2 FORCE=1
```

This should regenerate outputs even if cache exists.

## Failure Behavior

If a scene fails, the pipeline should:

- Mark the scene status as `failed`.
- Store error details in timeline.
- Continue if safe.
- Stop only on critical errors.

## Logging

Each stage should write logs to:

```text
data/logs/
```

Recommended files:

```text
data/logs/stage1_story.log
data/logs/stage2_images.log
data/logs/stage3_voice.log
data/logs/stage4_subtitles.log
data/logs/stage5_video.log
```

## Pipeline Philosophy

- Small stages.
- Clear inputs.
- Clear outputs.
- No hidden state.
- Cache expensive work.
- Never regenerate unnecessarily.
