#!/usr/bin/env bash
set -euo pipefail

# Determine the directory containing this script for both bash and zsh
if [ -n "${BASH_VERSION:-}" ]; then
  SCRIPT_PATH="${BASH_SOURCE[0]}"
elif [ -n "${ZSH_VERSION:-}" ]; then
  SCRIPT_PATH="${(%):-%x}"
else
  SCRIPT_PATH="$0"
fi

SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv"

if [ ! -d "$VENV_PATH" ]; then
  echo "Error: Virtual environment not found at $VENV_PATH. Run scripts/setup_venv.sh first." >&2
  exit 1
fi

# Deactivate an existing virtual environment if one is active
if [ -n "${VIRTUAL_ENV:-}" ]; then
  deactivate || true
fi

# shellcheck source=/dev/null
source "$VENV_PATH/bin/activate"

echo "Activated virtual environment located at $VENV_PATH"
