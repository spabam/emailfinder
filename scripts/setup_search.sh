#!/bin/bash
# Search Engine Email Checker Setup Script
# ========================================
#
# Copyright (c) 2015-2035 Andrea Bodei
# Email: info@andreabodei.com
# Version: 2.0.1.202510210253
#
# This script sets up the Search Engine Email Checker tool by creating a virtual environment
# and installing all required dependencies.
#
# WHAT THIS SCRIPT DOES:
# =====================
# 1. Creates a Python virtual environment in the user's home directory
# 2. Activates the virtual environment
# 3. Installs all required dependencies from requirements.txt
# 4. Provides usage instructions for the Search Engine Email Checker
#
# USAGE:
# ======
# ./setup_search.sh
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

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${YELLOW}$1${NC}"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

print_header "Search Engine Email Checker Setup"
echo "========================================"

# Use shared venv in home directory (outside Dropbox)
VENV_DIR="${RALPHCODE_VENV_DIR:-$HOME/.venv}"

# Create virtual environment if it doesn't exist
print_status "Setting up shared virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    print_status "Creating shared virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
    print_success "Virtual environment created successfully"
else
    print_status "Using existing shared virtual environment"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r data/requirements.txt

if [ $? -eq 0 ]; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Deactivate virtual environment
deactivate

print_success "Setup complete! To use the search engine email checker:"
echo ""
echo "1. Use the run script (recommended):"
echo "   ./run_search_email_checker.sh <domain>"
echo ""
echo "2. Or activate the virtual environment manually:"
echo "   source \${RALPHCODE_VENV_DIR:-$HOME/.venv}/bin/activate"
echo "   python search_email_checker.py <domain>"
echo "   deactivate"
echo ""
echo "3. Examples:"
echo "   ./run_search_email_checker.sh example.com"
echo "   ./run_search_email_checker.sh example.com google.com github.com"
echo "   ./run_search_email_checker.sh example.com --output emails.txt"
echo "   ./run_search_email_checker.sh --banner"
echo ""

