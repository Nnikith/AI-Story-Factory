# Voice Architecture

The voice subsystem is provider-based and local-first.

## Package

```text
app/voice/
  cache.py
  factory.py
  models.py
  providers/
    base.py
    placeholder.py
    kokoro.py
```

## Responsibilities

- Generate scene-level narration audio.
- Cache voice outputs.
- Update scene `audio_path`, `voice_metadata`, and voice status.

## Providers

Current providers:

- `placeholder`
- `kokoro`

## Kokoro

Kokoro is configured through `audio` settings:

```yaml
audio:
  voice_provider: "kokoro"
  voice_name: "af_heart"
  lang_code: "a"
  repo_id: "hexgrad/Kokoro-82M"
  sample_rate: 24000
```

## Rule

Stage 3 generates audio only. It does not create final subtitles unless word timing becomes available.
