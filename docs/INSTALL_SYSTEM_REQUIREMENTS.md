# System Requirements for cmps-357-audio-processing

## Docker Installation (Recommended)

The easiest way to run this application is using Docker, which handles all system dependencies automatically.

### Installing Docker

#### Linux (Ubuntu/Debian)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to the docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

#### macOS
1. Download and install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Launch Docker Desktop from Applications
3. Verify installation:
   ```bash
   docker --version
   docker compose version
   ```

#### Windows
1. Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Launch Docker Desktop
3. Verify installation in PowerShell or Command Prompt:
   ```powershell
   docker --version
   docker compose version
   ```

### Using Docker

Once Docker is installed, you can run the application without installing any other dependencies:

```bash
# Using Docker Compose (preferred)
docker compose up --build

# Or using Docker commands directly
docker build -t audio-processor .
docker run -d -p 5000:5000 --name audio-processor audio-processor
```

See the [README.md](../README.md) for more details on using Docker.

---

## Manual Installation (Alternative)

If you prefer not to use Docker, you can install dependencies manually. Before installing Python dependencies, ensure the following system packages and tools are installed:

## FFmpeg (Required)

FFmpeg is required by pydub for audio processing. This is the most critical system dependency.

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### macOS

Using Homebrew:
```bash
brew install ffmpeg
```

Download link (if not using Homebrew): https://ffmpeg.org/download.html

### Windows

**Option 1: Download Pre-built Binary (Recommended)**
1. Download FFmpeg from: https://ffmpeg.org/download.html
2. Choose a Windows build (e.g., from https://www.gyan.dev/ffmpeg/builds/)
3. Extract the ZIP file to a location like `C:\ffmpeg`
4. Add the `bin` folder to your system PATH:
   - Open "Environment Variables" in System Properties
   - Edit the "Path" variable under System variables
   - Add `C:\ffmpeg\bin` (or your installation path)
   - Click OK to save
5. Verify installation by opening Command Prompt and running: `ffmpeg -version`

**Option 2: Using Package Managers**
- **Chocolatey**: `choco install ffmpeg`
- **Scoop**: `scoop install ffmpeg`

## Python Development Libraries (Linux)

These packages are needed for building Python from source and for certain Python packages:

### Linux (Ubuntu/Debian)

```bash
sudo apt-get install libbz2-dev libsqlite3-dev
```

- **libbz2-dev**
  - Development headers and libraries for bzip2 compression. Required for building Python with bzip2 support and for some scientific packages.

- **libsqlite3-dev**
  - Development headers and libraries for SQLite3. Required for building Python with SQLite3 support and for database functionality in Python.

### macOS

These libraries are typically included with Xcode Command Line Tools:
```bash
xcode-select --install
```

### Windows

Not required on Windows. Python installers for Windows include necessary libraries.

## Python Version Management

### pyenv (Linux/macOS)

A tool for easily installing and managing multiple Python versions. Recommended for development environments where you need a specific Python version.

- Installation instructions: https://github.com/pyenv/pyenv#installation
- Install Python 3.12.0:
  ```bash
  pyenv install 3.12.0
  pyenv local 3.12.0
  ```

### Python 3.8 or Higher (Required)

- **Recommended**: Python 3.12.0
- Many scientific packages are not yet compatible with Python 3.13 or newer.

**Windows Python Installation:**
- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Verify installation: `python --version`

## Python Package Compatibility

- **Numpy**
  - For Python 3.12, you must use `numpy>=1.26.0` due to upstream compatibility changes. Older versions (e.g., 1.24.x) will not install or build correctly on Python 3.12.
  - This requirement is reflected in the project's `requirements.txt`.

## Quick Installation Guide

### Linux (Ubuntu/Debian)
```bash
# Install system requirements
sudo apt-get update
sudo apt-get install ffmpeg libbz2-dev libsqlite3-dev

# Install Python dependencies
pip install -r requirements.txt
```

### macOS
```bash
# Install FFmpeg
brew install ffmpeg

# Install Python dependencies
pip install -r requirements.txt
```

### Windows
```powershell
# Install FFmpeg (download and add to PATH as described above)
# Or use Chocolatey:
choco install ffmpeg

# Install Python dependencies
pip install -r requirements.txt
```

## Notes
- If you use pyenv, ensure your shell is configured to load pyenv (see `.zshrc` or `.bashrc` setup instructions).
- After installing these system requirements, you can proceed to set up your Python virtual environment and install project dependencies.
