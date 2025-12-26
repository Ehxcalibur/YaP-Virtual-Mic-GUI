#!/bin/bash

# Linux Virtual Mic Apps Launcher

APP_DIR="$(dirname "$(realpath "$0")")"
cd "$APP_DIR"

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Launching installer in terminal..."
    # Try to find a terminal emulator to run the installer
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal --wait -- ./install.sh
    elif command -v konsole &> /dev/null; then
        konsole --nofork -e ./install.sh
    elif command -v xfce4-terminal &> /dev/null; then
        xfce4-terminal --disable-server -x ./install.sh
    elif command -v x-terminal-emulator &> /dev/null; then
        x-terminal-emulator -e ./install.sh
    else
        # Fallback: hope we are in a terminal or install.sh can handle it (it likely can't without sudo pswd)
        ./install.sh
    fi
fi

echo ">>> Starting Void Mic..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
    
    # First Run Check
    if [ ! -f ".setup_done" ]; then
        echo ">>> Running first-time setup..."
        python3 src/setup_dialog.py
        touch .setup_done
    fi

    # Run in background, detached, suppressing output since we have no terminal
    nohup python3 main.py > /dev/null 2>&1 &
else
    echo "Installation failed or cancelled."
    exit 1
fi
