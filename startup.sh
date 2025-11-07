#!/bin/zsh

# 1. Check for venv/.venv, create .venv if missing
if [[ ! -d ".venv" && ! -d "venv" ]]; then
    echo "Creating Python virtual environment in .venv using pyenv's python..."
    python -m venv .venv
fi

# 2. Activate the virtual environment
if [[ -d ".venv" ]]; then
    source .venv/bin/activate
elif [[ -d "venv" ]]; then
    source venv/bin/activate
else
    echo "No virtual environment found. Exiting."
    exit 1
fi

# 3. Check for FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg is not installed. Please install it before continuing."
    exit 1
else
    echo "FFmpeg found."
fi

# 4. Install Python dependencies
if [[ -f "requirements.txt" ]]; then
    echo "Installing Python dependencies..."
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Exiting."
    exit 1
fi

# 5. Run the test suite
if [[ -f "test_app.py" ]]; then
    echo "Running test suite..."
    python -m pytest test_app.py -v || python test_app.py
else
    echo "test_app.py not found. Exiting."
    exit 1
fi
