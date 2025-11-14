# Docker on Windows — Quick Setup Notes

> **📌 DEPRECATED**: This document has been superseded by the comprehensive [DOCKER.md](DOCKER.md) guide.
> 
> Please refer to [DOCKER.md](DOCKER.md) for up-to-date Docker installation instructions for Windows, macOS, and Linux, including detailed Windows/WSL2 setup and troubleshooting.

---

**Legacy documentation preserved below for reference:**

This document summarizes the recommended steps used in this repo to get Docker Desktop + WSL2 working on Windows. It also explains the `wsl --install --no-distribution` prompt and troubleshooting tips.

## Quick recommended flow (Windows 10/11)

1. Open an elevated PowerShell (Run as Administrator) and install WSL2:
```powershell
# Simple install (installs WSL2 + Ubuntu)
wsl --install

# OR if you want WSL features enabled but prefer to install a distro manually:
wsl --install --no-distribution

# Ensure WSL default version is 2
wsl --set-default-version 2
```

2. If you used `--no-distribution`, install a distro afterwards (recommended: Ubuntu):
```powershell
# Example: install Ubuntu
wsl --install -d Ubuntu
```

3. Enable required Windows features (if not already enabled) and ensure hypervisor launches:
```powershell
# Enable if needed (requires reboot)
dism /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
# Optional: enable Hyper-V/Windows Hypervisor Platform for some setups
dism /online /enable-feature /featurename:Microsoft-Hyper-V-All /all /norestart

# Ensure hypervisor auto-start
bcdedit /set hypervisorlaunchtype auto

# Reboot after making these changes
shutdown /r /t 0
```

4. Install Docker Desktop for Windows (x86_64) from:
https://docs.docker.com/desktop/setup/install/windows-install/
- In Docker Desktop settings enable "Use the WSL 2 based engine" and enable integration for your distro.
- Sign out / restart Windows if installer prompts.

5. Verify everything:
```powershell
# From PowerShell or WSL shell
wsl --status
docker --version
docker compose version
docker run --rm hello-world
```

## What `wsl --install --no-distribution` means
- `--no-distribution` enables the WSL platform/components but does NOT install a Linux distribution.
- Use it if you want to enable WSL but install a distro manually (e.g., via Microsoft Store or `wsl --install -d <Distro>`).
- If you want the easiest path, run `wsl --install` (no `--no-distribution`) so WSL + default Ubuntu are installed automatically.

## Troubleshooting: "Virtualization support not detected" (even though Task Manager shows enabled)
- Common causes:
  - Hypervisor not set to launch on boot (run `bcdedit /set hypervisorlaunchtype auto` and reboot).
  - Core Isolation / Memory Integrity enabled — disable: Windows Security → Device security → Core isolation details → turn off Memory integrity, then reboot.
  - Conflicting virtualization software (older VirtualBox/VMware). Update or temporarily uninstall to test.
  - BIOS/UEFI settings — re-check VT-x / Virtualization support and re-save.
- Helpful checks:
```powershell
systeminfo | findstr /i "Hyper-V Requirements"
wsl --status
bcdedit /enum | findstr /i "hypervisorlaunchtype"
```
- After fixes, restart and re-open Docker Desktop → Troubleshoot → Run diagnostics if needed.

## Notes
- Use Docker Desktop + WSL2 for Linux-based images (this repo's Dockerfile uses python:3.12-slim).
- If you intentionally want Windows containers on Windows Server, enabling the Windows Containers feature is a different flow (Install-WindowsFeature / Add-WindowsFeature).
- If Docker Desktop still reports issues, collect Diagnostics from Docker Desktop → Troubleshoot and review logs.
