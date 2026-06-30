# Coding Standards

## Purpose

Keep AI Story Factory clean, maintainable, and easy to debug.

## Language

Primary language:

```text
Python 3.11+
```

Shell scripts are used for orchestration.

## Style

Use readable, simple Python.

Prefer clarity over cleverness.

## Project Rules

1. Every module should have one clear responsibility.
2. Pipeline stages should be independently runnable.
3. Expensive generated outputs should be cached.
4. Never hardcode machine-specific paths.
5. All paths should come from config.
6. All generated files should go under `data/output` or `data/cache`.
7. Large models should stay outside the repo.
8. The renderer should consume `timeline.json`.

## Python Formatting

Planned tools:

```text
ruff
black
isort
pytest
```

These can be added after the MVP starts working.

## Naming Conventions

Files:

```text
snake_case.py
```

Functions:

```text
snake_case()
```

Classes:

```text
PascalCase
```

Constants:

```text
UPPER_SNAKE_CASE
```

## Function Design

Good:

```python
def load_timeline(path: Path) -> Timeline:
    ...
```

Bad:

```python
def do_everything():
    ...
```

## Pipeline Stage Pattern

Each stage should follow this basic pattern:

```python
def run(config: Settings) -> None:
    timeline = load_timeline(config.paths.timeline)
    timeline = process(timeline, config)
    save_timeline(timeline, config.paths.timeline)
```

## Error Handling

Do not silently ignore errors.

For scene-level failures:

- Mark scene as failed.
- Store the error.
- Continue if possible.

For system-level failures:

- Stop the stage.
- Print a clear message.
- Write logs.

## Logging

Use structured, readable logs.

Examples:

```text
[Stage 2] Generating image for scene_001
[Stage 2] Cache hit for scene_002
[Stage 2] Failed scene_003: CUDA out of memory
```

## Type Hints

Use type hints for core modules.

Good:

```python
def split_story(text: str, max_scene_seconds: int) -> list[Scene]:
    ...
```

## Testing

At minimum:

- Smoke tests for full mini pipeline.
- Unit tests for utility functions.
- Integration tests for timeline stages.

## Commit Rule

Do not commit broken code to `main`.

Use `dev` or feature branches for active work.

## Scope Rule

Before adding a feature, ask:

```text
Does this help generate the first complete video?
```

If no, put it in `docs/LATER.md`.
