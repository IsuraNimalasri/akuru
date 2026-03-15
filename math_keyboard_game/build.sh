#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "== Happy Number Keys: build check =="

mkdir -p assets/images/robots assets/sounds data

if [[ "${1:-}" == "--with-robohash" ]]; then
  echo "Downloading RoboHash sample robots..."
  python3 download_robohash_images.py
fi

echo "Compiling python files..."
python3 -m py_compile \
  main.py \
  download_robohash_images.py \
  game/app.py \
  game/constants.py \
  game/levels.py \
  game/progress.py \
  game/widgets.py

echo "Build check complete."
echo "Run:"
echo "  python3 main.py"
