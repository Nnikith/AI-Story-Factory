#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# doctor.sh — Environment diagnostics for AI Story Factory
#
# Usage:
#   bash scripts/doctor.sh
#
# Checks:
# - repo structure
# - Python/venv
# - FFmpeg
# - CUDA/GPU visibility
# - required folders
# - config files
# - disk space
# ============================================================================

cd "$(dirname "$0")/.."
source scripts/lib.sh

EXIT_STATUS=0
ISSUES=()

add_issue() {
  EXIT_STATUS=1
  ISSUES+=("$1")
}

check_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    ok "$1 found"
  else
    fail "$1 missing"
    add_issue "$1 missing"
  fi
}

echo "${BOLD}🩺 Doctor — AI Story Factory Diagnostics${RESET}"

title "1) Required Commands"
check_cmd git
check_cmd python3
check_cmd ffmpeg
check_cmd ffprobe
check_cmd make

title "2) Repository Structure"

required_dirs=(
  app
  app/pipeline
  app/script
  app/scenes
  app/images
  app/voice
  app/subtitles
  app/renderer
  app/metadata
  assets
  assets/fonts
  assets/music
  configs
  data
  data/input
  data/output
  data/cache
  data/logs
  docs
  scripts
  tests
)

for d in "${required_dirs[@]}"; do
  [[ -d "$d" ]] && ok "Found $d" || { fail "Missing $d"; add_issue "missing $d"; }
done

required_files=(
  README.md
  PROJECT_PROPOSAL.md
  ROADMAP.md
  MILESTONES.md
  ARCHITECTURE.md
  TODO.md
  CHANGELOG.md
  Makefile
  requirements.txt
  pyproject.toml
  configs/default.yaml
)

for f in "${required_files[@]}"; do
  [[ -f "$f" ]] && ok "Found $f" || { warn "Missing $f"; add_issue "missing $f"; }
done

title "3) Git"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ok "Git repo detected"
  git status --short || true
else
  warn "Not a git repo yet"
  add_issue "not a git repo"
fi

if [[ -f ".gitignore" ]]; then
  ok ".gitignore present"
  grep -qE '(^|/)\.env(\s|$)' .gitignore && ok ".env is gitignored" || { warn ".env is not gitignored"; add_issue ".env not gitignored"; }
  grep -qE 'data/output|data/cache|models' .gitignore && ok "large/generated folders appear gitignored" || { warn "generated/model folders may not be gitignored"; add_issue "gitignore incomplete"; }
else
  warn ".gitignore missing"
  add_issue ".gitignore missing"
fi

title "4) Python"
PY="$(venv_python)"
ok "Python command: $PY"
"$PY" --version || { fail "Python failed"; add_issue "python failed"; }

if [[ -d ".venv" ]]; then
  ok ".venv exists"
else
  warn ".venv missing. Run: make setup"
  add_issue "venv missing"
fi

if [[ -f "requirements.txt" && -x ".venv/bin/python" ]]; then
  ".venv/bin/python" - <<'PY'
import importlib.util
mods = ["pydantic", "typer", "rich", "dotenv", "moviepy", "cv2", "pydub", "PIL"]
missing = [m for m in mods if importlib.util.find_spec(m) is None]
if missing:
    print("Missing Python packages:", ", ".join(missing))
    raise SystemExit(1)
print("Core Python packages import OK")
PY
  if [[ $? -eq 0 ]]; then ok "Python imports OK"; else add_issue "python packages missing"; fi
else
  info "Skipping package import check until .venv exists"
fi

title "5) FFmpeg"
ffmpeg -version | head -n 1 && ok "FFmpeg available" || { fail "FFmpeg failed"; add_issue "ffmpeg failed"; }
ffprobe -version | head -n 1 && ok "FFprobe available" || { fail "FFprobe failed"; add_issue "ffprobe failed"; }

title "6) GPU / CUDA"
if has_nvidia_gpu; then
  ok "NVIDIA GPU detected"
  show_gpu
else
  warn "nvidia-smi not available or GPU not visible to WSL"
  add_issue "gpu not visible"
fi

if [[ -x ".venv/bin/python" ]]; then
  set +e
  ".venv/bin/python" - <<'PY'
try:
    import torch
    print("torch:", torch.__version__)
    print("cuda available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("gpu:", torch.cuda.get_device_name(0))
except Exception as e:
    print("torch check skipped/failed:", e)
PY
  set -e
else
  info "Torch check skipped until .venv exists"
fi

title "7) Config"
[[ -f ".env" ]] && warn ".env exists; ensure secrets are not committed" || info ".env not present"
[[ -f ".env.example" ]] && ok ".env.example present" || warn ".env.example missing"
[[ -f "configs/default.yaml" ]] && ok "configs/default.yaml present" || { fail "configs/default.yaml missing"; add_issue "config missing"; }

title "8) Disk Space"
FREE_GB="$(disk_free_gb ".")"
info "Free space in project filesystem: ${FREE_GB} GB"
if (( FREE_GB < 30 )); then
  warn "Less than 30GB free. Video/image generation may fail."
  add_issue "low disk space"
else
  ok "Disk space looks acceptable"
fi

title "9) Summary"
if [[ "$EXIT_STATUS" -eq 0 ]]; then
  ok "All checks passed 🎉"
else
  fail "Issues detected"
  echo ""
  echo "${BOLD}Findings:${RESET}"
  for issue in "${ISSUES[@]}"; do
    echo " - $issue"
  done
fi

exit "$EXIT_STATUS"
