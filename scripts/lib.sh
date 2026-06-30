#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# lib.sh — Shared helpers for AI Story Factory scripts
# ============================================================================

RED=$'\033[31m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
BLUE=$'\033[34m'
BOLD=$'\033[1m'
RESET=$'\033[0m'

ok()    { echo "${GREEN}✅${RESET} $*"; }
warn()  { echo "${YELLOW}⚠️${RESET}  $*"; }
fail()  { echo "${RED}❌${RESET} $*" >&2; }
info()  { echo "${BLUE}ℹ️${RESET}  $*"; }
title() { echo ""; echo "${BOLD}$*${RESET}"; echo "-------------------------------------------------------------------------------"; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    fail "Missing required command: $1"
    exit 1
  }
}

repo_root() {
  git rev-parse --show-toplevel 2>/dev/null || pwd
}

cd_repo_root() {
  cd "$(repo_root)"
}

venv_python() {
  if [[ -x ".venv/bin/python" ]]; then
    echo ".venv/bin/python"
  else
    echo "python3"
  fi
}

venv_pip() {
  if [[ -x ".venv/bin/pip" ]]; then
    echo ".venv/bin/pip"
  else
    echo "pip3"
  fi
}

file_exists() {
  [[ -f "$1" ]]
}

dir_exists() {
  [[ -d "$1" ]]
}

ensure_dir() {
  mkdir -p "$1"
}

disk_free_gb() {
  local path="${1:-.}"
  df -BG "$path" | awk 'NR==2 {gsub("G","",$4); print $4}'
}

has_nvidia_gpu() {
  command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1
}

show_gpu() {
  if has_nvidia_gpu; then
    nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv,noheader
  else
    warn "No NVIDIA GPU detected through nvidia-smi"
  fi
}

wait_until() {
  local desc="$1"
  local timeout="${2:-60}"
  shift 2
  local start now

  start="$(date +%s)"
  info "Waiting up to ${timeout}s: ${desc}"

  while true; do
    if "$@" >/dev/null 2>&1; then
      ok "${desc}"
      return 0
    fi
    now="$(date +%s)"
    if (( now - start >= timeout )); then
      fail "Timeout waiting for: ${desc}"
      return 1
    fi
    sleep 2
  done
}

confirm_destructive() {
  local prompt="${1:-This is destructive. Continue?}"
  echo "${YELLOW}${prompt}${RESET}"
  read -r -p "Type YES to continue: " answer
  [[ "$answer" == "YES" ]]
}

load_env_file() {
  if [[ -f ".env" ]]; then
    # shellcheck disable=SC1091
    set -a
    source ".env"
    set +a
  fi
}
