#!/bin/bash
# Whois Email Checker Runner Script
# =================================
#
# Copyright (c) 2015-2035 Andrea Bodei
# Email: info@andreabodei.com
# Version: 2.0.1.202510210253
#
# This script activates the Whois Email Checker virtual environment and runs the
# whois email checker tool with all provided command line arguments.
#
# WHAT THIS SCRIPT DOES:
# =====================
# 1. Checks if the Whois Email Checker virtual environment exists
# 2. Activates the virtual environment
# 3. Runs the whois email checker with all provided arguments
# 4. Passes through all command line arguments to the Python script
#
# USAGE:
# ======
# ./run_whois_email_checker.sh <domain> [options]
#
# EXAMPLES:
# =========
# ./run_whois_email_checker.sh example.com
# ./run_whois_email_checker.sh example.com google.com github.com
# ./run_whois_email_checker.sh example.com --output emails.txt
# ./run_whois_email_checker.sh --banner
#
# REQUIREMENTS:
# ============
# - Virtual environment must be set up using ./setup_whois.sh first
# - Whois Email Checker Python script must be present
#
# LICENSE:
# ========
# This script is provided as-is for educational and security assessment purposes.
# Use responsibly and in accordance with applicable laws and regulations.

# Use shared venv in home directory (outside Dropbox)
VENV_DIR="${RALPHCODE_VENV_DIR:-$HOME/.venv}"

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/whois_email_checker.py"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Please run ./setup_whois.sh first."
    exit 1
fi

# Activate virtual environment and run the script
source "$VENV_DIR/bin/activate"
python "$PYTHON_SCRIPT" "$@"
