#!/bin/bash
# EmailHarvester Email Checker Setup Script
# =========================================
# Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
# Version: 2.0.1.202510210253
# 
# This script sets up the EmailHarvester email checker environment.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    EmailHarvester Email Checker Setup                      ║${NC}"
echo -e "${BLUE}║                                                                              ║${NC}"
echo -e "${BLUE}║  Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com                ║${NC}"
echo -e "${BLUE}║  Version: 2.0.1.202510210253                                                  ║${NC}"
echo -e "${BLUE}║                                                                              ║${NC}"
echo -e "${BLUE}║  This script sets up the EmailHarvester email checker environment.          ║${NC}"
echo -e "${BLUE}║                                                                              ║${NC}"
echo -e "${BLUE}║  SECURITY NOTE: Use responsibly and in accordance with applicable laws      ║${NC}"
echo -e "${BLUE}║  and regulations. Always obtain proper authorization before testing.        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Python 3 is available
echo -e "${BLUE}🔍 Checking Python 3 installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python 3 found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo -e "${YELLOW}💡 Please install Python 3.6 or higher${NC}"
    exit 1
fi

# Check if pip3 is available
echo -e "${BLUE}🔍 Checking pip3 installation...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 found${NC}"
else
    echo -e "${RED}❌ pip3 is not installed${NC}"
    echo -e "${YELLOW}💡 Please install pip3${NC}"
    exit 1
fi

# Use shared venv in home directory (outside Dropbox)
VENV_DIR="${RALPHCODE_VENV_DIR:-$HOME/.venv}"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${BLUE}📦 Creating shared virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}📦 Activating shared virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Install required Python packages
echo -e "${BLUE}📦 Installing required Python packages...${NC}"

# Check if requests is already installed
if python3 -c "import requests" 2>/dev/null; then
    echo -e "${GREEN}✅ requests library already installed${NC}"
else
    echo -e "${YELLOW}📥 Installing requests library...${NC}"
    pip install requests
    echo -e "${GREEN}✅ requests library installed${NC}"
fi

# Install EmailHarvester
echo -e "${BLUE}📦 Installing EmailHarvester...${NC}"
if command -v emailharvester &> /dev/null || python3 -c "import emailharvester" 2>/dev/null; then
    echo -e "${GREEN}✅ EmailHarvester already installed${NC}"
else
    echo -e "${YELLOW}📥 Installing EmailHarvester...${NC}"
    pip install emailharvester
    echo -e "${GREEN}✅ EmailHarvester installed${NC}"
fi

# Deactivate virtual environment
deactivate

# Verify installation
echo -e "${BLUE}🔍 Verifying installation...${NC}"

# Test Python script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/emailharvester_checker.py"

if [ -f "$PYTHON_SCRIPT" ]; then
    echo -e "${GREEN}✅ EmailHarvester checker script found${NC}"
    
    # Test script execution
    if python3 "$PYTHON_SCRIPT" --banner >/dev/null 2>&1; then
        echo -e "${GREEN}✅ EmailHarvester checker script is working${NC}"
    else
        echo -e "${RED}❌ EmailHarvester checker script has issues${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ EmailHarvester checker script not found${NC}"
    exit 1
fi

# Test runner script
RUNNER_SCRIPT="$SCRIPT_DIR/run_emailharvester_checker.sh"

if [ -f "$RUNNER_SCRIPT" ]; then
    echo -e "${GREEN}✅ EmailHarvester checker runner script found${NC}"
    
    # Make runner script executable
    chmod +x "$RUNNER_SCRIPT"
    echo -e "${GREEN}✅ EmailHarvester checker runner script is executable${NC}"
else
    echo -e "${RED}❌ EmailHarvester checker runner script not found${NC}"
    exit 1
fi

# Test EmailHarvester installation
echo -e "${BLUE}🔍 Testing EmailHarvester installation...${NC}"
if command -v emailharvester &> /dev/null; then
    echo -e "${GREEN}✅ EmailHarvester is accessible${NC}"
else
    echo -e "${YELLOW}⚠️  EmailHarvester not found in PATH${NC}"
    echo -e "${BLUE}💡 You may need to add ~/.local/bin to your PATH${NC}"
    echo -e "${BLUE}   Add this to your ~/.bashrc: export PATH=\$PATH:~/.local/bin${NC}"
fi

echo ""
echo -e "${GREEN}🎉 EmailHarvester Email Checker setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}📋 USAGE EXAMPLES:${NC}"
echo -e "${YELLOW}  # Basic EmailHarvester email search${NC}"
echo -e "  ./run_emailharvester_checker.sh example.com"
echo ""
echo -e "${YELLOW}  # With output file${NC}"
echo -e "  ./run_emailharvester_checker.sh example.com --output emails.txt"
echo ""
echo -e "${YELLOW}  # JSON output${NC}"
echo -e "  ./run_emailharvester_checker.sh example.com --output emails.json"
echo ""
echo -e "${YELLOW}  # Verbose output${NC}"
echo -e "  ./run_emailharvester_checker.sh example.com --verbose"
echo ""
echo -e "${YELLOW}  # Show banner${NC}"
echo -e "  ./run_emailharvester_checker.sh --banner"
echo ""
echo -e "${BLUE}📚 For more information, run:${NC}"
echo -e "  ./run_emailharvester_checker.sh --help"
echo ""
echo -e "${GREEN}✅ Setup complete! You can now use the EmailHarvester Email Checker.${NC}"

