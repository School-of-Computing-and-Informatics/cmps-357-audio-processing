# Docker Setup and Usage Guide

This guide provides comprehensive instructions for installing and using Docker to run the audio processing application. Docker is the **recommended** way to run this application as it handles all system dependencies automatically.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installing Docker](#installing-docker)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Running the Application](#running-the-application)
- [Docker Commands Reference](#docker-commands-reference)
- [Troubleshooting](#troubleshooting)

## Overview

Docker packages the application with all its dependencies (Python, FFmpeg, system libraries) into a container, eliminating the need to install these components on your local machine. This ensures consistent behavior across different operating systems and simplifies setup.

### Prerequisites

- **Windows**: Windows 10 version 2004+ or Windows 11 (with WSL 2 support)
- **macOS**: macOS 10.15 or newer
- **Linux**: Any modern Linux distribution (Ubuntu, Debian, Fedora, etc.)
- **Hardware**: Virtualization support enabled in BIOS/UEFI

## Quick Start

Once Docker is installed (see platform-specific instructions below):

```bash
# Clone the repository (if not already done)
git clone https://github.com/School-of-Computing-and-Informatics/cmps-357-audio-processing.git
cd cmps-357-audio-processing

# Build and start the application
docker compose up --build

# Access the application at http://localhost:5000
```

The application will start automatically and be available at `http://localhost:5000`.

## Installing Docker

### Windows

Docker on Windows requires Windows Subsystem for Linux 2 (WSL2) for optimal performance.

#### Step 1: Install WSL 2

Open PowerShell as Administrator and run:

```powershell
# Install WSL2 with Ubuntu (recommended for most users)
wsl --install

# Set WSL 2 as the default version
wsl --set-default-version 2

# Reboot your computer
shutdown /r /t 0
```

After reboot, Ubuntu will open and prompt you to create a username and password. Complete this setup.

**Alternative**: If you want to install WSL without a distribution initially:
```powershell
wsl --install --no-distribution
```
Then install your preferred distribution later:
```powershell
wsl --install -d Ubuntu
```

#### Step 2: Verify WSL Installation

```powershell
# Check WSL status
wsl --status

# List installed distributions
wsl --list --verbose
```

Ensure your distribution is running on WSL 2 (version 2 in the output).

#### Step 3: Install Docker Desktop

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow the prompts
3. When prompted, ensure "Use WSL 2 instead of Hyper-V" is checked
4. Restart your computer if prompted

#### Step 4: Configure Docker Desktop

1. Launch Docker Desktop from the Start menu
2. Go to Settings → General
3. Ensure "Use the WSL 2 based engine" is enabled
4. Go to Settings → Resources → WSL Integration
5. Enable integration with your Ubuntu distribution
6. Click "Apply & Restart"

#### Step 5: Verify Installation

Open PowerShell or Windows Terminal:

```powershell
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Test Docker installation
docker run --rm hello-world
```

If you see "Hello from Docker!", your installation is successful.

#### Windows Troubleshooting

**Problem: "Virtualization is not enabled"**
- Solution: Enable virtualization in BIOS/UEFI
  1. Restart computer and enter BIOS (usually F2, F10, or Del during boot)
  2. Look for "Virtualization Technology", "Intel VT-x", or "AMD-V"
  3. Enable the setting and save changes

**Problem: "WSL 2 installation is incomplete"**
- Solution: Ensure Windows features are enabled
  ```powershell
  # Run as Administrator
  dism /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
  dism /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
  
  # Ensure hypervisor launches on startup
  bcdedit /set hypervisorlaunchtype auto
  
  # Reboot
  shutdown /r /t 0
  ```

**Problem: "Docker Desktop won't start"**
- Check system requirements: Windows 10 version 2004+ or Windows 11
- Disable "Memory Integrity" in Windows Security:
  1. Open Windows Security → Device Security
  2. Click "Core isolation details"
  3. Turn off "Memory integrity"
  4. Restart computer
- Ensure no conflicting virtualization software (older VirtualBox/VMware versions)

**Problem: "Access denied" or permission errors**
- Add your user to the docker-users group:
  1. Open Computer Management (Win+X → Computer Management)
  2. Go to Local Users and Groups → Groups
  3. Double-click "docker-users"
  4. Add your username
  5. Log out and log back in

**Additional Resources:**
- Check Docker Desktop logs: Settings → Troubleshoot → Download diagnostics
- Run diagnostics: Docker Desktop → Troubleshoot → Run diagnostics

### macOS

#### Step 1: Install Docker Desktop

1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
   - For Apple Silicon (M1/M2/M3): Choose "Mac with Apple chip"
   - For Intel Macs: Choose "Mac with Intel chip"
2. Open the downloaded `.dmg` file
3. Drag Docker.app to your Applications folder
4. Launch Docker Desktop from Applications

#### Step 2: Complete First-Time Setup

1. Docker Desktop will request permissions for system extensions
2. Click "OK" and enter your password when prompted
3. Wait for Docker Desktop to start (whale icon in menu bar will be steady)

#### Step 3: Verify Installation

Open Terminal:

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Test Docker installation
docker run --rm hello-world
```

#### macOS Troubleshooting

**Problem: "Docker Desktop requires privileged access"**
- This is normal. Enter your macOS password to allow system extensions

**Problem: Docker commands not found**
- Ensure Docker Desktop is running (check menu bar for whale icon)
- Restart Terminal after installation

**Problem: Docker Desktop won't start**
- Check System Preferences → Security & Privacy → General
- Allow system extensions from Docker
- Restart computer if needed

**Problem: Performance issues**
- Allocate more resources in Docker Desktop settings:
  - Settings → Resources
  - Increase CPUs and Memory as needed
  - Apply & Restart

### Linux

Docker installation on Linux is straightforward and doesn't require additional virtualization layers.

#### Ubuntu/Debian

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
sudo docker --version
sudo docker compose version
```

**Alternative (Quick Install Script):**
```bash
# Download and run Docker's convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify installation
sudo docker --version
sudo docker compose version
```

#### Fedora/RHEL/CentOS

```bash
# Install dnf plugins
sudo dnf -y install dnf-plugins-core

# Add Docker repository
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Install Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
sudo docker --version
sudo docker compose version
```

#### Arch Linux

```bash
# Install Docker
sudo pacman -S docker docker-compose

# Start Docker service
sudo systemctl start docker.service
sudo systemctl enable docker.service

# Verify installation
sudo docker --version
sudo docker compose version
```

#### Post-Installation Steps (All Linux Distributions)

**Run Docker without sudo (recommended):**

```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Apply group changes (or log out and back in)
newgrp docker

# Test without sudo
docker run --rm hello-world
```

**Enable Docker to start on boot:**

```bash
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

#### Linux Troubleshooting

**Problem: "Permission denied" when running docker commands**
- Ensure you're in the docker group: `groups $USER`
- If not, add yourself: `sudo usermod -aG docker $USER`
- Log out and back in, or run: `newgrp docker`

**Problem: Docker daemon not running**
- Start the service: `sudo systemctl start docker`
- Check status: `sudo systemctl status docker`
- View logs: `sudo journalctl -u docker`

**Problem: "Cannot connect to the Docker daemon"**
- Ensure Docker service is running: `sudo systemctl start docker`
- Check if Docker socket exists: `ls -l /var/run/docker.sock`

## Running the Application

### Using Docker Compose (Recommended)

Docker Compose simplifies running multi-container applications and is the easiest way to get started.

```bash
# Start the application (builds if needed)
docker compose up --build

# Run in detached mode (background)
docker compose up -d --build

# View logs
docker compose logs -f

# Stop the application
docker compose down

# Stop and remove volumes
docker compose down -v
```

The application will be available at: **http://localhost:5000**

### Using Docker Commands Directly

If you prefer not to use Docker Compose:

```bash
# Build the image
docker build -t audio-processor .

# Run the container
docker run -d -p 5000:5000 --name audio-processor audio-processor

# View logs
docker logs -f audio-processor

# Stop the container
docker stop audio-processor

# Remove the container
docker rm audio-processor

# Remove the image
docker rmi audio-processor
```

### Development Mode

For development with live code reloading:

```bash
# The docker-compose.yml already mounts the source directory
# Just start with compose
docker compose up

# In another terminal, you can exec into the container
docker compose exec audio_app bash

# Or run tests inside the container
docker compose exec audio_app python -m pytest tests/ -v
```

## Docker Commands Reference

### Common Commands

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List images
docker images

# Remove a container
docker rm <container-name-or-id>

# Remove an image
docker rmi <image-name-or-id>

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove everything (containers, images, volumes, networks)
docker system prune -a

# View container logs
docker logs <container-name>

# Execute command in running container
docker exec -it <container-name> bash

# Inspect container
docker inspect <container-name>

# View container resource usage
docker stats
```

### Docker Compose Commands

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Build/rebuild services
docker compose build

# Build and start
docker compose up --build

# Stop services
docker compose stop

# Start stopped services
docker compose start

# Restart services
docker compose restart

# Stop and remove containers
docker compose down

# View logs
docker compose logs

# Follow logs
docker compose logs -f

# Execute command in service
docker compose exec audio_app bash

# List running services
docker compose ps
```

## Troubleshooting

### General Issues

**Problem: Port 5000 already in use**
```bash
# Find process using port 5000
# Linux/Mac:
sudo lsof -i :5000

# Windows:
netstat -ano | findstr :5000

# Kill the process or change port in docker-compose.yml
# Edit docker-compose.yml and change "5000:5000" to "8080:5000"
```

**Problem: Build fails with "no space left on device"**
```bash
# Clean up Docker resources
docker system prune -a --volumes

# Check available disk space
df -h
```

**Problem: Container exits immediately**
```bash
# Check logs for errors
docker compose logs

# Or for standalone container
docker logs audio-processor
```

**Problem: Changes to code not reflected in container**
```bash
# Rebuild the image
docker compose up --build

# Or force recreate
docker compose up --force-recreate --build
```

**Problem: Cannot connect to application at localhost:5000**
- Verify container is running: `docker compose ps`
- Check container logs: `docker compose logs`
- Ensure port mapping is correct in docker-compose.yml
- Try accessing from http://127.0.0.1:5000 instead

### Performance Issues

**Slow builds:**
- Use `.dockerignore` to exclude unnecessary files
- Leverage Docker layer caching (avoid changing files that trigger rebuilds)
- Use multi-stage builds (already implemented in this project)

**Slow application:**
- Allocate more resources to Docker (Docker Desktop → Settings → Resources)
- On Windows, ensure WSL 2 integration is properly configured
- Check that files are in WSL filesystem, not Windows filesystem (Windows only)

### Getting Help

If you encounter issues not covered here:

1. Check Docker Desktop diagnostics (Settings → Troubleshoot)
2. View application logs: `docker compose logs -f`
3. Check Docker daemon status (Linux): `sudo systemctl status docker`
4. Consult the [Docker documentation](https://docs.docker.com/)
5. Search for or create an issue in the project repository

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/install/)
- [Docker Desktop for Mac](https://docs.docker.com/desktop/mac/install/)
- [Docker Engine for Linux](https://docs.docker.com/engine/install/)
- [WSL 2 Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
