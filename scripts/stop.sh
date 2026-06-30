#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# stop.sh — Stop AI Story Factory background processes
#
# Currently this project has no required daemon processes. This script is kept
# so future services such as ComfyUI, local TTS server, or API workers can be
# stopped from one place.
# ============================================================================

cd "$(dirname "$0")/.."
source scripts/lib.sh

title "🛑 Stopping AI Story Factory services"

# Future examples:
# pkill -f "comfyui" || true
# pkill -f "uvicorn app.main" || true

ok "No background services configured yet"
ok "Stop completed"
