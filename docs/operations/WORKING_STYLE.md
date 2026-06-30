# Working Style

## Rules

1. Small milestones first.
2. Commit regularly.
3. Do not add features unless they help the current milestone.
4. Put future ideas in `docs/LATER.md`.
5. Use Makefile commands whenever possible.
6. Keep generated outputs out of Git.
7. Build the 60-second MVP before attempting long videos.

## Daily Workflow

```bash
git pull
make check
# work
make demo
git add .
git commit -m "Clear commit message"
git push
```

## Scope Control Question

Before adding anything, ask:

```text
Does this help generate the first complete video?
```

If no, move it to `docs/LATER.md`.
