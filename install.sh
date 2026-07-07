#!/usr/bin/env bash

set -e

echo "Starting SATube installation..."
echo "──────────────────────────────────────"

# 1. Install system requirements based on the package manager
if command -v pacman &> /dev/null; then
    echo "Arch Linux detected. Installing system requirements..."
    sudo pacman -S --needed ffmpeg python-pipx
elif command -v apt-get &> /dev/null; then
    echo "Debian/Ubuntu detected. Installing system requirements..."
    sudo apt-get update
    sudo apt-get install -y ffmpeg pipx
elif command -v dnf &> /dev/null; then
    echo "Fedora detected. Installing system requirements..."
    sudo dnf install -y ffmpeg pipx
else
    echo "Warning: Could not detect package manager."
    echo "Please ensure 'ffmpeg' and 'pipx' are installed manually before continuing."
    sleep 2
fi

# 2. Ensure pipx is in the system PATH
echo "Ensuring pipx is in your PATH..."
pipx ensurepath

# 3. Install the application and its Python dependencies
echo "Installing SATube and Python dependencies via pipx..."
pipx install --force .

echo "──────────────────────────────────────"
echo "Installation complete!"
echo ""
echo "Note: If this is your first time using pipx, you may need to reload your shell path:"
echo "Run: source ~/.bashrc (or source ~/.zshrc)"
echo ""
echo "Then simply type 'satube' to launch the application."