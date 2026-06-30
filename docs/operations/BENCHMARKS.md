# Benchmarks

Track performance of expensive stages.

## Current Metrics

Recommended metrics:

- Stage 2 image generation time
- Stage 3 voice generation time
- Stage 5 render time
- cache hit/miss behavior
- final video size

## Commands

```bash
grep -R "elapsed=" data/logs/
```

## Notes

Local AI image generation and first-time model downloads are expected to be slower than cached runs.
