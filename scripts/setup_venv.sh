#!/usr/bin/env bash
set -euo pipefail

# Resolve project root relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Error: $PYTHON_BIN is not available on the PATH." >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  "$PYTHON_BIN" -m venv .venv
  echo "Created virtual environment at .venv using $PYTHON_BIN."
else
  echo "Virtual environment .venv already exists; reusing it."
fi

# shellcheck source=/dev/null
source .venv/bin/activate
python -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "requirements.txt not found; installing core dependencies explicitly."
  pip install pandas requests yfinance plotly
fi

deactivate

echo "Virtual environment setup complete. Activate it with: source scripts/activate_venv.sh"
