# Email Finder Installer Script

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The Email Finder Installer Script (`installer.sh`) sets up the shared Python virtual environment and installs the base dependencies required by the Email Finder Suite. It creates a venv in the user home directory and installs packages from `data/requirements.txt`.

This installer covers the core Python dependencies for the web, whois, and search checkers. Tool-specific components (EmailHarvester, TheHarvester, GPG, etc.) have their own setup scripts under `scripts/`.

## Features

- **Shared Virtual Environment**: Creates/uses `$HOME/vantage_venv`
- **Base Dependency Install**: Installs requirements from `data/requirements.txt`
- **Simple Setup**: One-command installation

## Prerequisites

- Bash shell
- Python 3.6 or higher
- pip package manager
- Internet connection for downloading dependencies

## Usage

```bash
./installer.sh
```

## Recommended Follow-Up

Run tool-specific setup scripts for the components you plan to use:

```bash
./scripts/setup_whois.sh
./scripts/setup_search.sh
./scripts/setup_gpg.sh
./scripts/setup_emailharvester.sh
./scripts/setup_theharvester.sh
```

## What It Installs

- **Virtual environment**: `$HOME/vantage_venv`
- **Python packages**: from `data/requirements.txt`

## Troubleshooting

### Python Not Found
```
Error: Python 3.6+ not found
```
**Fix**: Install Python 3.6+ and retry.

### Permission Denied
```
Error: Permission denied
```
**Fix**:
```bash
chmod +x installer.sh
```

### Dependency Installation Failed
```
Error: Failed to install dependencies
```
**Fix**: Check internet connectivity and pip configuration.

## Integration Example

```bash
#!/bin/bash
# Complete email finder suite setup

./installer.sh
./scripts/setup_whois.sh
./scripts/setup_search.sh
./scripts/setup_gpg.sh
./scripts/setup_emailharvester.sh
./scripts/setup_theharvester.sh
```
