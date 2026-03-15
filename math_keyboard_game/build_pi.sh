#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "== Raspberry Pi build: Happy Number Keys =="

mkdir -p assets/images/robots assets/sounds data

if [[ "${1:-}" == "--with-robohash" ]]; then
  echo "Downloading RoboHash sample robots..."
  python3 download_robohash_images.py
fi

echo "Checking Python files..."
python3 -m py_compile \
  main.py \
  download_robohash_images.py \
  game/app.py \
  game/constants.py \
  game/levels.py \
  game/progress.py \
  game/widgets.py

echo "Marking scripts executable..."
chmod +x install_pi.sh run_game.sh build_pi.sh install.sh build.sh || true

echo "Build complete."
echo "Next step:"
echo "  ./install_pi.sh"
