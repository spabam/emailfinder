#!/bin/bash
# Whois Email Checker Setup Script
# ================================
#
# Copyright (c) 2015-2035 Andrea Bodei
# Email: info@andreabodei.com
# Version: 2.0.1.202510210253
#
# This script sets up the Whois Email Checker tool by creating a virtual environment
# and installing all required dependencies.
#
# WHAT THIS SCRIPT DOES:
# =====================
# 1. Creates a Python virtual environment in the user's home directory
# 2. Activates the virtual environment
# 3. Installs all required dependencies from requirements.txt
# 4. Provides usage instructions for the Whois Email Checker
#
# USAGE:
# ======
# ./setup_whois.sh
#
# REQUIREMENTS:
# ============
# - Python 3.6+
# - pip package manager
# - whois command-line tool
# - Internet connection for downloading dependencies
#
# LICENSE:
# ========
# This script is provided as-is for educational and security assessment purposes.
# Use responsibly and in accordance with applicable laws and regulations.

echo "Whois Email Checker Setup"
echo "========================="

# Check if whois command is available
if ! command -v whois &> /dev/null; then
    echo "Warning: whois command not found. Please install whois package:"
    echo "  Ubuntu/Debian: sudo apt-get install whois"
    echo "  CentOS/RHEL: sudo yum install whois"
    echo "  macOS: brew install whois"
    echo ""
fi

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
echo "Setup complete! To use the whois email checker:"
echo ""
echo "1. Use the run script (recommended):"
echo "   ./run_whois_email_checker.sh <domain>"
echo ""
echo "2. Or activate the virtual environment manually:"
echo "   source \${RALPHCODE_VENV_DIR:-$HOME/.venv}/bin/activate"
echo "   python whois_email_checker.py <domain>"
echo "   deactivate"
echo ""
echo "3. Examples:"
echo "   ./run_whois_email_checker.sh example.com"
echo "   ./run_whois_email_checker.sh example.com google.com github.com"
echo "   ./run_whois_email_checker.sh example.com --output emails.txt"
echo "   ./run_whois_email_checker.sh --banner"
echo ""

