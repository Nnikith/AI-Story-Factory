# Release Process

## Branch Flow

```text
feature/*
  ↓
dev
  ↓
main
  ↓
tag
  ↓
GitHub Release
```

## Checklist

```bash
git status
python -m compileall app
make clean-output
make demo
```

Merge to `dev`:

```bash
git switch dev
git pull origin dev
git merge feature/<branch>
make clean-output
make demo
git push origin dev
```

Merge to `main`:

```bash
git switch main
git pull origin main
git merge dev
make clean-output
make demo
git push origin main
```

Tag:

```bash
git tag -a vX.Y.Z -m "Release title"
git push origin vX.Y.Z
```

Then create a GitHub Release from the tag.
