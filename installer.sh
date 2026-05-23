#!/bin/bash
# Email Finder Installer Script
# =============================
#
# Copyright (c) 2015-2035 Andrea Bodei
# Email: info@andreabodei.com
# Version: 2.0.1.202510210253
#
# This script sets up the core Email Finder environment by creating a shared
# virtual environment and installing the base dependencies.
#
# WHAT THIS SCRIPT DOES:
# =====================
# 1. Creates a Python virtual environment in the user's home directory
# 2. Activates the virtual environment
# 3. Installs all required dependencies from requirements.txt
# 4. Provides usage instructions for the Email Finder tools
#
# USAGE:
# ======
# ./installer.sh
#
# REQUIREMENTS:
# ============
# - Python 3.6+
# - pip package manager
# - Internet connection for downloading dependencies
#
# LICENSE:
# ========
# This script is provided as-is for educational and security assessment purposes.
# Use responsibly and in accordance with applicable laws and regulations.

echo "Email Finder Installer"
echo "======================"

# Use shared venv in home directory (outside Dropbox)
VENV_DIR="${RALPHCODE_VENV_DIR:-$HOME/.venv}"

# Check if virtual environment exists (create if needed)
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating shared virtual environment in home directory..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install -r data/requirements.txt

echo ""
echo "Setup complete! To use the email finder tools:"
echo ""
echo "1. Use the run scripts (recommended):"
echo "   ./scripts/run_email_checker.sh <url>"
echo "   ./run_enumeration.sh <target>"
echo ""
echo "2. Or activate the virtual environment manually:"
echo "   source \${RALPHCODE_VENV_DIR:-$HOME/.venv}/bin/activate"
echo "   python scripts/email_checker.py <url>"
echo "   deactivate"
echo ""
echo "3. Examples:"
echo "   ./scripts/run_email_checker.sh https://example.com"
echo "   ./scripts/run_email_checker.sh https://example.com --max-depth 3"
echo "   ./scripts/run_email_checker.sh https://example.com --output emails.txt"
echo "   ./scripts/run_email_checker.sh --banner"
echo ""
