# Scene Planning

Scene planning converts story text into structured scene plans.

## Package

```text
app/scenes/
  factory.py
  models.py
  providers/
    base.py
    heuristic.py
```

## Responsibilities

- split story text into scene narration chunks
- estimate scene duration
- assign mood and camera defaults
- request image prompts from the prompt subsystem
- return planned scenes to the timeline builder

## Current Provider

- `heuristic`

## Configuration

```yaml
scene_planning:
  provider: "heuristic"
  max_scene_chars: 220
```

## Future Providers

- local LLM scene planner
- screenplay planner
- semantic scene splitter
