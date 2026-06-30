#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# smoke.sh — End-to-end lightweight smoke test
#
# Goal:
#   story.txt → scenes.json → images → silent audio → subtitles → render placeholder
# ============================================================================

cd "$(dirname "$0")/.."
source scripts/lib.sh

title "🧪 Smoke Test — AI Story Factory"

PY="$(venv_python)"

title "1) Required commands"
need_cmd ffmpeg
need_cmd ffprobe
"$PY" --version

title "2) Required input"
if [[ ! -f "data/input/story.txt" ]]; then
  warn "data/input/story.txt missing. Creating sample."
  mkdir -p data/input
  cat > data/input/story.txt <<'EOF'
A young hero wakes up in a strange fantasy world with a mysterious pendant. The pendant glows, revealing a hidden power that could turn his poor village into a powerful empire.
EOF
fi
ok "Input story exists"

title "3) Run pipeline placeholders"

if [[ -f "scripts/placeholder_scenes.py" ]]; then
  "$PY" scripts/placeholder_scenes.py
else
  fail "scripts/placeholder_scenes.py missing"
  exit 1
fi

if [[ -f "scripts/placeholder_images.py" ]]; then
  "$PY" scripts/placeholder_images.py
else
  fail "scripts/placeholder_images.py missing"
  exit 1
fi

if [[ -f "scripts/placeholder_voice.py" ]]; then
  "$PY" scripts/placeholder_voice.py
else
  fail "scripts/placeholder_voice.py missing"
  exit 1
fi

if [[ -f "scripts/placeholder_subtitles.py" ]]; then
  "$PY" scripts/placeholder_subtitles.py
else
  fail "scripts/placeholder_subtitles.py missing"
  exit 1
fi

if [[ -f "scripts/placeholder_render.py" ]]; then
  "$PY" scripts/placeholder_render.py
else
  fail "scripts/placeholder_render.py missing"
  exit 1
fi

title "4) Verify outputs"
[[ -f "data/output/scenes.json" ]] && ok "scenes.json created" || { fail "scenes.json missing"; exit 1; }
[[ -d "data/output/images" ]] && ok "images folder exists" || { fail "images folder missing"; exit 1; }
[[ -f "data/output/audio/narration.wav" ]] && ok "narration.wav created" || { fail "narration.wav missing"; exit 1; }
[[ -f "data/output/subtitles/subtitles.srt" ]] && ok "subtitles.srt created" || { fail "subtitles.srt missing"; exit 1; }

if [[ -f "data/output/videos/demo.mp4" ]]; then
  ok "demo.mp4 created"
elif [[ -f "data/output/videos/demo_placeholder.txt" ]]; then
  warn "Render placeholder exists; real MP4 renderer not implemented yet"
else
  fail "No render output found"
  exit 1
fi

ok "Smoke tests passed"
