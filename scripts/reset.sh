#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# reset.sh — Reset generated outputs/cache and rerun start
#
# Usage:
#   bash scripts/reset.sh
#
# Env vars:
#   WIPE_CACHE=1|0
# ============================================================================

cd "$(dirname "$0")/.."
source scripts/lib.sh

WIPE_CACHE="${WIPE_CACHE:-0}"

title "♻️ Reset AI Story Factory"

warn "This removes generated output files."
if ! confirm_destructive "Remove data/output contents?"; then
  warn "Reset cancelled"
  exit 0
fi

rm -rf data/output/*
ensure_dir data/output/images
ensure_dir data/output/audio
ensure_dir data/output/subtitles
ensure_dir data/output/videos

if [[ "$WIPE_CACHE" == "1" ]]; then
  warn "WIPE_CACHE=1 — removing data/cache contents"
  rm -rf data/cache/*
fi

ok "Generated outputs reset"

RUN_SMOKE=1 bash scripts/start.sh
ok "Reset completed"
