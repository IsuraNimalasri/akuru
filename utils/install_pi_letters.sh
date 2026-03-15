#!/bin/bash
set -e

echo "=== Installing Letters as desktop app ==="

INSTALL_DIR="$HOME/.local/share/letters"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Check executable exists
if [ ! -f "dist/letters" ]; then
    echo "ERROR: dist/letters not found. Run ./utils/build_pi_letters.sh first."
    exit 1
fi

# Create directories
mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$DESKTOP_DIR"

# Copy executable and icon
cp dist/letters "$INSTALL_DIR/letters"
chmod +x "$INSTALL_DIR/letters"

if [ -f "akuru.png" ]; then
    cp akuru.png "$INSTALL_DIR/letters.png"
fi

# Symlink to bin
ln -sf "$INSTALL_DIR/letters" "$BIN_DIR/letters"

# Create desktop entry
cat > "$DESKTOP_DIR/letters.desktop" << EOF
[Desktop Entry]
Name=Letters (English Typing)
Comment=Practice typing English letters
Exec=$INSTALL_DIR/letters
Icon=$INSTALL_DIR/letters.png
Terminal=false
Type=Application
Categories=Education;
StartupNotify=true
EOF

echo ""
echo "=== Installed! ==="
echo "You can now:"
echo "  - Find 'Letters (English Typing)' in the application menu under Education"
echo "  - Or run 'letters' from the terminal"
