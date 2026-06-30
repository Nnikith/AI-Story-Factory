#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# start.sh — Start/check local AI Story Factory dev environment
#
# This does not start heavy model servers yet. It prepares folders, checks tools,
# and optionally runs a smoke test.
#
# Env vars:
#   RUN_SMOKE=1|0
# ============================================================================

cd "$(dirname "$0")/.."
source scripts/lib.sh

RUN_SMOKE="${RUN_SMOKE:-1}"

title "🚀 Starting AI Story Factory dev environment"

info "Loading .env if present"
load_env_file

title "1) Create required folders"
folders=(
  data/input
  data/output
  data/output/images
  data/output/audio
  data/output/subtitles
  data/output/videos
  data/cache
  data/logs
  assets/fonts
  assets/music
)
for d in "${folders[@]}"; do
  ensure_dir "$d"
  ok "Ready: $d"
done

title "2) Environment check"
bash scripts/doctor.sh || {
  warn "Doctor reported issues. Fix them before long runs."
}

title "3) Optional smoke test"
if [[ "$RUN_SMOKE" == "1" ]]; then
  bash scripts/smoke.sh
else
  info "RUN_SMOKE=0 set — skipping smoke test"
fi

ok "Start completed"
