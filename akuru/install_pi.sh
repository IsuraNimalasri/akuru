#!/bin/bash
set -e

echo "=== Installing Akuru as desktop app ==="

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

INSTALL_DIR="$HOME/.local/share/akuru"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Check executable exists
if [ ! -f "dist/akuru" ]; then
    echo "ERROR: dist/akuru not found. Run ./akuru/build_pi.sh first."
    exit 1
fi

# Create directories
mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$DESKTOP_DIR"

# Copy executable and icon
cp dist/akuru "$INSTALL_DIR/akuru"
chmod +x "$INSTALL_DIR/akuru"

if [ -f "akuru.png" ]; then
    cp akuru.png "$INSTALL_DIR/akuru.png"
fi

# Symlink to bin
ln -sf "$INSTALL_DIR/akuru" "$BIN_DIR/akuru"

# Create desktop entry
cat > "$DESKTOP_DIR/akuru.desktop" << EOF
[Desktop Entry]
Name=අකුරු (Akuru)
Comment=Learn to write Sinhala letters
Exec=$INSTALL_DIR/akuru
Icon=$INSTALL_DIR/akuru.png
Terminal=false
Type=Application
Categories=Education;
StartupNotify=true
EOF

echo ""
echo "=== Installed! ==="
echo "You can now:"
echo "  - Find 'අකුරු (Akuru)' in the application menu under Education"
echo "  - Or run 'akuru' from the terminal"
