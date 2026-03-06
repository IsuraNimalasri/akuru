#!/bin/bash
set -e

echo "=== Akuru - Clean Rebuild & Reinstall ==="
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

INSTALL_DIR="$HOME/.local/share/akuru"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# 1. Remove old installed app
echo "[1/3] Removing old installation..."
rm -rf "$INSTALL_DIR"
rm -f "$BIN_DIR/akuru"
rm -f "$DESKTOP_DIR/akuru.desktop"
echo "  Old installation removed."

# 2. Remove old build artifacts and rebuild
echo "[2/3] Cleaning old build and rebuilding..."
rm -rf build/ dist/ *.spec
./utils/build_pi.sh

# 3. Reinstall
echo "[3/3] Installing new version..."
./utils/install_pi.sh

echo ""
echo "=== Done! Akuru has been rebuilt and reinstalled. ==="
