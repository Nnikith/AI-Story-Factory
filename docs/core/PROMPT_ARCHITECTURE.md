# Prompt Architecture

Prompt generation is provider-based and separated from scene planning.

## Package

```text
app/prompts/
  factory.py
  models.py
  providers/
    base.py
    default.py
```

## Responsibilities

- turn scene text, mood, and style into image prompts
- generate negative prompts
- expose prompt metadata

## Configuration

```yaml
prompts:
  image_provider: "default"
  image_style: "cinematic anime fantasy"
```

## Rule

Scene planners should not hardcode image prompt text. They should call the prompt provider.
