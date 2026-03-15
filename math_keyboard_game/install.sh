#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "== Happy Number Keys: install =="

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Please install Python 3 first."
  exit 1
fi

echo "Python: $(python3 --version)"

# Tkinter is normally bundled on Raspberry Pi OS with python3-tk.
if ! python3 - <<'PY'
import tkinter
print("tkinter ok")
PY
then
  echo "Tkinter not available."
  echo "On Raspberry Pi OS run: sudo apt-get install -y python3-tk"
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

echo "Activating venv and installing requirements..."
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Install complete."
echo "Run game with:"
echo "  cd \"$SCRIPT_DIR\""
echo "  source .venv/bin/activate"
echo "  python3 main.py"
