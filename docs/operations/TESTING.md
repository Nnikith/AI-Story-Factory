# Testing

## Basic Validation

```bash
python -m compileall app
make clean-output
make demo
```

## Stage-Level Validation

```bash
make stage1
make stage2
make stage3
make stage4
make stage5
```

## Expected Outputs

```text
data/output/timeline.json
data/output/images/
data/output/audio/
data/output/subtitles/subtitles.srt
data/output/videos/demo.mp4
```

## Current Minimum Acceptance Test

A change is acceptable when:

- Python compiles
- `make demo` succeeds
- generated video exists
- timeline metadata is preserved
