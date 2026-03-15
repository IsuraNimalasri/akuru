#!/bin/bash
set -e

echo "=== Letters - Raspberry Pi Build ==="
echo ""

# Check we're on Linux (Pi)
if [[ "$(uname)" != "Linux" ]]; then
    echo "ERROR: This script must be run on the Raspberry Pi (Linux)."
    echo "Copy this project to your Pi first, then run this script there."
    exit 1
fi

# Install system dependencies
echo "[1/4] Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq python3-tk python3-venv python3-pip fonts-noto-core

# Create virtual environment
echo "[2/4] Setting up Python environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

# Install PyInstaller
echo "[3/4] Installing PyInstaller..."
pip install --quiet pyinstaller

# Build executable
echo "[4/4] Building executable..."
pyinstaller \
    --onefile \
    --windowed \
    --name letters \
    --add-data "letters:letters" \
    letters/main.py

echo ""
echo "=== Build complete! ==="
echo "Executable: dist/letters"
echo ""
echo "To install as a desktop app, run:"
echo "  ./utils/install_pi_letters.sh"
