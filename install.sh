#!/bin/bash

# Linux Virtual Mic GUI App Installer
# Handles dependency installation for Debian, Fedora, Arch, and openSUSE

set -e

echo ">>> Detecting Distribution..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    LIKE=$ID_LIKE
else
    echo "Cannot detect distribution. Exiting."
    exit 1
fi

echo "Detected Distribution: $DISTRO (Like: $LIKE)"

install_pkgs() {
    echo ">>> Installing system dependencies..."
    case "$1" in
        debian|ubuntu|linuxmint|pop)
            sudo apt update
            sudo apt install -y mpv ffmpeg pulseaudio-utils python3-pip libmpv-dev python3-venv
            ;;
        fedora)
            sudo dnf check-update || true
            sudo dnf install -y mpv ffmpeg pulseaudio-utils python3-pip mpv-libs python3-virtualenv
            ;;
        arch|manjaro|endeavouros)
            sudo pacman -Syu --noconfirm
            sudo pacman -S --noconfirm mpv ffmpeg libpulse python-pip yt-dlp
            ;;
        opensuse*|suse)
            sudo zypper refresh
            sudo zypper install -y mpv ffmpeg pulseaudio-utils python3-pip libmpv1 python3-virtualenv
            ;;
        *)
            echo "Unsupported distribution family. Returning to basic check."
            # Fallback attempts could go here, but for now we error out or rely on user to have deps
            echo "Please ensure mpv, ffmpeg, pulseaudio-utils, and python3-venv are installed."
            ;;
    esac
}

# Determine package manager family
if [[ "$DISTRO" == "debian" || "$DISTRO" == "ubuntu" || "$LIKE" == *"debian"* || "$LIKE" == *"ubuntu"* ]]; then
    install_pkgs "debian"
elif [[ "$DISTRO" == "fedora" || "$LIKE" == *"fedora"* ]]; then
    install_pkgs "fedora"
elif [[ "$DISTRO" == "arch" || "$LIKE" == *"arch"* ]]; then
    install_pkgs "arch"
elif [[ "$DISTRO" == *"opensuse"* || "$LIKE" == *"suse"* ]]; then
    install_pkgs "opensuse"
else
    echo "Unknown distribution. Attempting generic install logic could be dangerous. Skipping system packages."
    echo "Please manually install: mpv, ffmpeg, pulseaudio-utils, python3-venv."
fi

echo ">>> Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo ".venv created."
else
    echo ".venv already exists."
fi

echo ">>> Installing Python dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ">>> Making launcher executable..."
chmod +x launch.sh

echo ">>> Installation Complete! Run ./launch.sh to start the app."
