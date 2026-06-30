#!/usr/bin/env bash
set -Eeuo pipefail

# ============================================================================
# git_commit.sh — Auto/custom commit helper for AI Story Factory
#
# Usage:
#   make commit
#   make commit MSG="your custom message"
#   bash scripts/git_commit.sh "your custom message"
# ============================================================================

cd "$(git rev-parse --show-toplevel)"

echo "=========================================================="
echo "[0] Repo + tool sanity"
echo "=========================================================="

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git not found in PATH."
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: This folder is not a git repo."
  exit 1
fi

echo "OK: git repo detected"
echo

echo "=========================================================="
echo "[1] Current changes"
echo "=========================================================="
git status
echo
git status --porcelain
echo

if [[ $# -gt 0 ]]; then
  COMMIT_MSG="$*"
elif [[ -n "${MSG:-}" ]]; then
  COMMIT_MSG="$MSG"
else
  if command -v python3 >/dev/null 2>&1; then
    TS="$(python3 -c "from datetime import datetime; print(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))")"
  else
    TS="$(date +"%Y-%m-%d_%H-%M-%S")"
  fi
  COMMIT_MSG="[Auto] Update ${TS}"
fi

mkdir -p .git
MSGFILE=".git/COMMIT_MSG_TMP.txt"
printf "%s\n" "$COMMIT_MSG" > "$MSGFILE"

echo "=========================================================="
echo "[2] Commit message"
echo "=========================================================="
cat "$MSGFILE"
echo

echo "=========================================================="
echo "[3] Stage changes"
echo "=========================================================="
git add .
echo "--- Staged files ---"
git diff --name-only --cached
echo

if git diff --cached --quiet; then
  echo "=========================================================="
  echo "[4] Nothing staged - no commit needed"
  echo "=========================================================="
  rm -f "$MSGFILE"
  exit 0
fi

echo "=========================================================="
echo "[4] Commit"
echo "=========================================================="
if ! git commit -F "$MSGFILE"; then
  echo "ERROR: git commit failed."
  echo "Common fixes:"
  echo "  git config --global user.name \"Your Name\""
  echo "  git config --global user.email \"you@example.com\""
  rm -f "$MSGFILE"
  exit 1
fi

echo
echo "=========================================================="
echo "[5] Push"
echo "=========================================================="
if git remote -v | grep -q .; then
  git push || {
    echo "WARN: git push failed. Commit was created locally."
    rm -f "$MSGFILE"
    exit 1
  }
else
  echo "No git remote configured. Skipping push."
fi

rm -f "$MSGFILE"
echo
echo "Done."
