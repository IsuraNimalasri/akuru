#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

APP_NAME="Happy Number Keys"
APP_ID="happy-number-keys"
DESKTOP_FILE_NAME="${APP_ID}.desktop"
ICON_PATH="$SCRIPT_DIR/logo.png"
RUN_PATH="$SCRIPT_DIR/run_game.sh"

USER_HOME="${HOME}"
APPLICATIONS_DIR="${USER_HOME}/.local/share/applications"
DESKTOP_DIR="${USER_HOME}/Desktop"

echo "== Raspberry Pi install: ${APP_NAME} =="

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Install Python 3 first."
  exit 1
fi

if ! python3 - <<'PY'
import tkinter
print("tkinter ok")
PY
then
  echo "Tkinter is missing."
  echo "Install with: sudo apt-get update && sudo apt-get install -y python3-tk"
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

echo "Installing Python dependencies..."
# shellcheck disable=SC1091
source ".venv/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

chmod +x "$RUN_PATH"

mkdir -p "$APPLICATIONS_DIR"
mkdir -p "$DESKTOP_DIR"

DESKTOP_CONTENT="[Desktop Entry]
Type=Application
Version=1.0
Name=${APP_NAME}
Comment=Keyboard maths game for kids
Exec=${RUN_PATH}
Path=${SCRIPT_DIR}
Icon=${ICON_PATH}
Terminal=false
Categories=Education;Game;
Keywords=math;kids;learning;keyboard;
StartupNotify=true
"

echo "$DESKTOP_CONTENT" > "${APPLICATIONS_DIR}/${DESKTOP_FILE_NAME}"
echo "$DESKTOP_CONTENT" > "${DESKTOP_DIR}/${DESKTOP_FILE_NAME}"

chmod +x "${APPLICATIONS_DIR}/${DESKTOP_FILE_NAME}"
chmod +x "${DESKTOP_DIR}/${DESKTOP_FILE_NAME}"

echo "Installed desktop launcher:"
echo "  ${APPLICATIONS_DIR}/${DESKTOP_FILE_NAME}"
echo "  ${DESKTOP_DIR}/${DESKTOP_FILE_NAME}"
echo ""
echo "You can now open '${APP_NAME}' from the Raspberry Pi menu or Desktop."
