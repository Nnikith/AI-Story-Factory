#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# bootstrap.sh — One-time setup for a fresh machine/repo
# ============================================================================

cd "$(dirname "$0")/.."
source scripts/lib.sh

title "🧰 Bootstrap AI Story Factory"

title "1) System commands"
need_cmd python3
need_cmd git
need_cmd make

if ! command -v ffmpeg >/dev/null 2>&1; then
  warn "ffmpeg missing."
  warn "Install on Ubuntu/WSL: sudo apt update && sudo apt install -y ffmpeg"
else
  ok "ffmpeg found"
fi

title "2) Python virtual environment"
if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
  ok "Created .venv"
else
  ok ".venv already exists"
fi

.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

title "3) Folders"
bash scripts/start.sh RUN_SMOKE=0 || true

title "4) Script permissions"
chmod +x scripts/*.sh
ok "Scripts executable"

title "5) Git"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ok "Git repo already initialized"
else
  git init
  ok "Initialized git repo"
fi

ok "Bootstrap completed"
