# Git Workflow

## Branches

Main stable branch:

```text
main
```

Development branch:

```text
dev
```

Feature branches:

```text
feature/story-parser
feature/image-generation
feature/subtitles
feature/video-renderer
```

Docs branches:

```text
docs/project-standards
```

## Recommended Flow

```bash
git checkout dev
git pull
git checkout -b feature/story-parser
# work
make smoke
make commit MSG="[Pipeline] Add Stage 1 story parser"
git checkout dev
git merge feature/story-parser
git push
```

## Commit Message Format

Use:

```text
[Type] Short description
```

Allowed types:

```text
[Init]
[Docs]
[Config]
[Pipeline]
[Feature]
[Images]
[Voice]
[Subtitles]
[Renderer]
[Metadata]
[Models]
[Performance]
[Refactor]
[Fix]
[Test]
[CI]
[Release]
```

Examples:

```text
[Docs] Add timeline schema
[Pipeline] Add Stage 1 timeline generator
[Images] Add SDXL prompt builder
[Voice] Add local TTS backend
[Renderer] Burn subtitles into video
[Fix] Correct output path handling
```

## Daily Git Commands

Check status:

```bash
git status
```

Commit with helper:

```bash
make commit MSG="[Docs] Update roadmap"
```

Push:

```bash
git push
```

## First Repo Setup

```bash
git init
git branch -M main
git remote add origin git@github.com:Nnikith/AI-Story-Factory.git
git push -u origin main
```

## Create Dev Branch

```bash
git checkout -b dev
git push -u origin dev
```

## Tags

Use tags for milestones.

```bash
git tag -a v0.0.1 -m "Project scaffold"
git push origin v0.0.1
```

Planned tags:

```text
v0.0.1 project scaffold
v0.1.0 60-second MVP
v0.2.0 local image generation
v0.3.0 real voice generation
v0.4.0 first watchable video
v1.0.0 complete automated pipeline
```

## Main Branch Rule

`main` should always be stable.

Before merging to `main`:

```bash
make doctor
make smoke
```

Both should pass.

## What Not to Commit

Never commit:

```text
.env
data/output/
data/cache/
models/
large videos
generated images
generated audio
API keys
```

## GitHub Issues

Use Issues for tasks instead of letting `TODO.md` become too large.

Suggested initial issues:

```text
#1 Timeline schema implementation
#2 Stage 1 story parser
#3 Placeholder renderer
#4 Subtitle engine
#5 Local image backend
#6 Voice backend
```

## GitHub Releases

Create a GitHub Release for important milestones.

Example:

```text
v0.1.0 — First 60-second MVP
```
