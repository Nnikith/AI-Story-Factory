# Script Commands

## One-time setup

```bash
make bootstrap
```

or:

```bash
make setup
make chmod
```

## Daily workflow

```bash
make doctor
make smoke
make commit MSG="[Docs] Update project scripts"
```

## Main commands

```bash
make doctor   # check environment
make start    # prepare project and run smoke test
make smoke    # run lightweight pipeline test
make demo     # run placeholder demo pipeline
make render   # render demo MP4 if renderer exists
make stop     # stop background services
make reset    # delete generated outputs and rerun start
make commit   # commit and push
```

## Important rule

Generated files stay out of Git:

- `data/output/`
- `data/cache/`
- `models/`
- video/image/audio outputs
