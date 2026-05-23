#!/bin/bash
# EmailHarvester Email Checker Runner Script
# ==========================================
# Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
# Version: 2.0.1.202510210253
# 
# This script runs the EmailHarvester email checker with proper
# environment setup and error handling.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/emailharvester_checker.py"

# Use shared venv in home directory (outside Dropbox)
VENV_DIR="${RALPHCODE_VENV_DIR:-$HOME/.venv}"
VENV_PY="$VENV_DIR/bin/python"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}❌ Error: EmailHarvester checker script not found at: $PYTHON_SCRIPT${NC}"
    exit 1
fi

# Function to show usage
show_usage() {
    echo "EmailHarvester Email Checker Runner Script"
    echo "=========================================="
    echo ""
    echo "Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com"
    echo ""
    echo "This script runs the EmailHarvester email checker with proper"
    echo "environment setup and error handling."
    echo ""
    echo "USAGE:"
    echo "  $0 <domain> [options]"
    echo ""
    echo "ARGUMENTS:"
    echo "  domain                 Domain to search for (required)"
    echo ""
    echo "OPTIONS:"
    echo "  --output FILE          Output file path (supports .txt, .json, .csv)"
    echo "  --verbose              Enable verbose output"
    echo "  --timeout SECONDS      Command timeout in seconds (default: 30)"
    echo "  --help                 Show this help message"
    echo ""
    echo "EXAMPLES:"
    echo "  # Basic EmailHarvester email search"
    echo "  $0 example.com"
    echo ""
    echo "  # With output file"
    echo "  $0 example.com --output emails.txt"
    echo ""
    echo "  # JSON output"
    echo "  $0 example.com --output emails.json"
    echo ""
    echo "  # Verbose output"
    echo "  $0 example.com --verbose"
    echo ""
    echo "  # Show banner"
    echo "  $0 --banner"
    echo ""
    echo "REQUIREMENTS:"
    echo "  - Python 3.6+"
    echo "  - EmailHarvester tool installed"
    echo "  - Internet connection for email discovery"
    echo ""
    echo "Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com"
}

# Check for help or banner
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_usage
    exit 0
fi

if [ "$1" = "--banner" ]; then
    if [ ! -x "$VENV_PY" ]; then
        echo -e "${RED}❌ Error: Virtual environment not found at: $VENV_DIR${NC}"
        echo -e "${BLUE}💡 Please run ./setup_emailharvester.sh first${NC}"
        exit 1
    fi
    "$VENV_PY" "$PYTHON_SCRIPT" --banner
    exit 0
fi

# Check if domain is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ Error: Domain is required${NC}"
    echo ""
    show_usage
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}❌ Error: Virtual environment not found at: $VENV_DIR${NC}"
    echo -e "${BLUE}💡 Please run ./setup_emailharvester.sh first${NC}"
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Check if EmailHarvester is available
if ! command -v emailharvester &> /dev/null; then
    echo -e "${YELLOW}⚠️  Warning: EmailHarvester not found in PATH${NC}"
    echo -e "${BLUE}💡 Please install EmailHarvester first${NC}"
    echo -e "${BLUE}   You can install it using: ./setup_emailharvester.sh${NC}"
fi

# Run the EmailHarvester email checker
echo -e "${BLUE}🚀 Starting EmailHarvester Email Checker...${NC}"
echo ""

# Execute the Python script with all arguments
python "$PYTHON_SCRIPT" "$@"

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ EmailHarvester email search completed successfully${NC}"
else
    echo ""
    echo -e "${RED}❌ EmailHarvester email search failed${NC}"
    exit 1
fi
