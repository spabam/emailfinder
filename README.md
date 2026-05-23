# Email Finder Suite

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The Email Finder Suite is a comprehensive collection of tools for discovering email addresses from multiple sources. This suite provides powerful email discovery capabilities for legitimate security assessments, contact information gathering, and compliance checking.

## Directory Structure

```
email_finder/
├── README.md                    # This file - main documentation
├── installer.sh                 # Core dependency installer
├── run_enumeration.sh           # Main execution script
├── scripts/                     # All Python and shell scripts
│   ├── Python Scripts/
│   │   ├── email_checker.py
│   │   ├── whois_email_checker.py
│   │   ├── search_email_checker.py
│   │   ├── gpg_email_checker.py
│   │   ├── emailharvester_checker.py
│   │   ├── theharvester_checker.py
│   │   ├── web_email_finder.py
│   │   └── test_working_tools.py
│   ├── Shell Scripts/
│   │   ├── run_email_checker.sh
│   │   ├── run_whois_email_checker.sh
│   │   ├── run_search_email_checker.sh
│   │   ├── run_gpg_email_checker.sh
│   │   ├── run_emailharvester_checker.sh
│   │   └── run_theharvester_checker.sh
│   ├── Setup Scripts/
│   │   ├── setup_emailharvester.sh
│   │   ├── setup_gpg.sh
│   │   ├── setup_search.sh
│   │   ├── setup_theharvester.sh
│   │   └── setup_whois.sh
│   └── Documentation/
│       ├── README_email_checker.md
│       ├── README_whois_email_checker.md
│       ├── README_search_email_checker.md
│       ├── README_gpg_email_checker.md
│       ├── README_emailharvester_checker.md
│       ├── README_theharvester_checker.md
│       ├── README_web_email_finder.md
│       ├── README_test_working_tools.md
│       ├── README_run_enumeration.md
│       ├── README_run_email_checker.md
│       └── README_setup.md
├── data/                        # Data files and test results
│   ├── requirements.txt
│   ├── *.txt, *.csv, *.json
│   └── test data files
├── reports/                     # Documentation and reports
│   ├── README.md (original)
│   ├── *.md report files
│   └── integration reports
└── logs/                        # Log files (created during execution)
```

## Tools Included

### 1. Web Email Checker (`scripts/email_checker.py`)
- **Purpose**: Crawls websites and extracts email addresses from all pages
- **Features**: Multi-threaded processing, advanced email extraction, validation
- **Documentation**: `scripts/README_email_checker.md`

### 2. Whois Email Checker (`scripts/whois_email_checker.py`)
- **Purpose**: Extracts email addresses from whois data for domain registration information
- **Features**: Domain and IP whois queries, email validation, multiple output formats
- **Documentation**: `scripts/README_whois_email_checker.md`

### 3. Search Engine Email Checker (`scripts/search_email_checker.py`)
- **Purpose**: Searches Google, DuckDuckGo, and Yahoo for email addresses related to a domain
- **Features**: Multi-search engine support, rate limiting, comprehensive reporting
- **Documentation**: `scripts/README_search_email_checker.md`

### 4. GPG/PGP Email Checker (`scripts/gpg_email_checker.py`)
- **Purpose**: Searches GPG key servers for email addresses associated with a domain
- **Features**: Multi-server support, key metadata extraction, email validation
- **Documentation**: `scripts/README_gpg_email_checker.md`

### 5. EmailHarvester Email Checker (`scripts/emailharvester_checker.py`)
- **Purpose**: Uses EmailHarvester to find email addresses associated with a domain
- **Features**: EmailHarvester integration, comprehensive email discovery, multiple outputs
- **Documentation**: `scripts/README_emailharvester_checker.md`

### 6. TheHarvester Email Checker (`scripts/theharvester_checker.py`)
- **Purpose**: Uses TheHarvester to find email addresses associated with a domain
- **Features**: TheHarvester integration, comprehensive email discovery, multiple outputs
- **Documentation**: `scripts/README_theharvester_checker.md`

### 7. Web Email Finder (`scripts/web_email_finder.py`)
- **Purpose**: Finds email addresses by scraping websites and searching for email patterns
- **Features**: Reliable web scraping, pattern matching, multiple output formats
- **Documentation**: `scripts/README_web_email_finder.md`

### 8. Test Working Tools (`scripts/test_working_tools.py`)
- **Purpose**: Tests all email finder tools to verify functionality
- **Features**: Automated testing, performance measurement, error detection
- **Documentation**: `scripts/README_test_working_tools.md`

## Quick Start

### 1. Installation
```bash
# Install core dependencies and create the shared venv
./installer.sh

# Optional: install tool-specific dependencies
./scripts/setup_whois.sh
./scripts/setup_search.sh
./scripts/setup_gpg.sh
./scripts/setup_emailharvester.sh
./scripts/setup_theharvester.sh
```
The installer creates a shared virtual environment at `~/vantage_venv`.

### 2. Basic Usage
```bash
# Run all email finders on a target
./run_enumeration.sh example.com

# Run individual tools
./scripts/run_email_checker.sh https://example.com
./scripts/run_whois_email_checker.sh example.com
```

### 3. Testing
```bash
# Test all tools
python3 scripts/test_working_tools.py
```

## Main Scripts

### Installer Script (`installer.sh`)
- **Purpose**: Sets up the shared virtual environment and base dependencies
- **Features**: Virtual environment creation, dependency installation
- **Documentation**: `scripts/README_setup.md`

### Main Runner Script (`run_enumeration.sh`)
- **Purpose**: Runs the core email finding tools sequentially and merges results
- **Features**: Complete tool orchestration, output merging, automatic retry on non-zero exit codes, silent-by-default with `--verbose`/`--debug` for full output
- **Documentation**: `scripts/README_run_enumeration.md`

## Individual Tool Runners

Each tool has its own runner script in the `scripts/` directory:
- `run_email_checker.sh` - Web email checker runner
- `run_whois_email_checker.sh` - Whois email checker runner
- `run_search_email_checker.sh` - Search engine email checker runner
- `run_gpg_email_checker.sh` - GPG email checker runner
- `run_emailharvester_checker.sh` - EmailHarvester checker runner
- `run_theharvester_checker.sh` - TheHarvester checker runner

## Setup Scripts

Individual setup scripts for specific tools:
- `setup_emailharvester.sh` - EmailHarvester installation
- `setup_gpg.sh` - GPG tools installation
- `setup_search.sh` - Search tools setup
- `setup_theharvester.sh` - TheHarvester installation
- `setup_whois.sh` - Whois tools setup

## Output and Results

### Generated Files
- **Text Output**: Simple lists of discovered email addresses
- **CSV Output**: Structured data with source information
- **JSON Output**: Detailed information including metadata
- **Log Files**: Execution logs and error information

### File Locations
- **Results**: Generated in current directory or specified output directory
- **Logs/Temp**: Per-run temp files and tool logs in `/tmp/email_finders_<pid>/` (run_enumeration)
- **Data**: Test data and configuration files in `data/` directory
- **Reports**: Documentation and reports in `reports/` directory

## Security Considerations

### Legal Notice
This tool suite is intended for authorized security testing only. Users must:
- Obtain proper authorization before searching for email addresses
- Comply with all applicable laws and regulations
- Respect rate limits and usage policies
- Use responsibly and ethically

### Best Practices
- Always obtain proper authorization before use
- Respect tool rate limits and terms of service
- Use appropriate delays between requests
- Follow responsible disclosure practices

## Troubleshooting

### Common Issues
1. **Tool Not Found**: Ensure all tools are properly installed
2. **Permission Denied**: Check script permissions (`chmod +x script.sh`)
3. **Dependency Issues**: Run setup script to install dependencies
4. **Network Issues**: Check internet connectivity and firewall settings

### Getting Help
1. Check individual tool documentation in `scripts/` directory
2. Review error messages and logs
3. Verify tool installation and configuration
4. Test with known working domains

## Performance

### Optimization Tips
- Use appropriate timeout values for your network
- Monitor system resources during execution
- Use single targets for faster results
- Consider using individual tools for specific needs

### Resource Usage
- **Memory**: 50-500MB depending on tool and target
- **CPU**: Low to moderate usage during execution
- **Network**: Varies based on tool and target
- **Storage**: Minimal, only for output files

## Integration

### Script Integration
```bash
#!/bin/bash
# Example integration script

TARGET="example.com"
OUTPUT_DIR="./results"

# Run comprehensive email discovery
./run_enumeration.sh "$TARGET" --output-dir "$OUTPUT_DIR"

# Process results
process_email_results "$OUTPUT_DIR"
```

### Automation
```bash
#!/bin/bash
# Automated email discovery

TARGETS=("example.com" "google.com" "github.com")

for target in "${TARGETS[@]}"; do
    echo "Discovering emails for $target..."
    ./run_enumeration.sh "$target" --output-dir "./results/$target"
done
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**

## Shared Virtual Environment Standard
All scripts in this project are standardized to use one shared Python virtual environment:
`/home/spabam/.venv`

You can optionally override this path with:
`RALPHCODE_VENV_DIR=/home/spabam/.venv`
