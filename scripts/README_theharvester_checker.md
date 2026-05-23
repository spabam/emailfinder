# TheHarvester Email Checker

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The TheHarvester Email Checker (`theharvester_checker.py`) is a specialized tool that uses TheHarvester to find email addresses associated with a domain. It leverages TheHarvester's powerful email discovery capabilities for comprehensive email enumeration.

## Features

### Core Capabilities
- **TheHarvester Integration**: Uses TheHarvester tool for email discovery
- **Email Extraction**: Extracts email addresses from TheHarvester output
- **Email Validation**: Validates extracted email addresses for proper format
- **Deduplication**: Removes duplicate email addresses automatically
- **Multiple Output Formats**: Supports text, CSV, and JSON output formats
- **Comprehensive Reporting**: Detailed statistics and analysis

### Advanced Features
- **Batch Processing**: Processes multiple domains in a single run
- **Error Handling**: Robust error handling with detailed logging
- **Statistics Reporting**: Comprehensive statistics on discovered emails
- **Tool Integration**: Seamless integration with TheHarvester
- **Output Processing**: Advanced processing of TheHarvester results

## Installation

### Prerequisites
- Python 3.6 or higher
- TheHarvester tool installed
- Internet connectivity

### Dependencies
```bash
# Install TheHarvester
git clone https://github.com/laramies/theHarvester.git
cd theHarvester
pip install -r requirements.txt

# Python dependencies
pip install requests
```

## Usage

### Basic Usage
```bash
python3 theharvester_checker.py <domain>
```

### Advanced Usage
```bash
python3 theharvester_checker.py <domain> [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output file path | auto-generated |
| `--format` | Output format (txt, csv, json) | txt |
| `--batch` | Batch file with multiple domains | None |
| `--verbose` | Verbose output | False |
| `--theharvester-path` | Path to TheHarvester tool | auto-detect |

## Examples

### Single Domain Search
```bash
python3 theharvester_checker.py example.com
```

### Custom Output Format
```bash
python3 theharvester_checker.py example.com --format json --output theharvester_emails.json
```

### Batch Processing
```bash
python3 theharvester_checker.py --batch domains.txt --format csv
```

### Advanced Configuration
```bash
python3 theharvester_checker.py example.com --theharvester-path /path/to/theHarvester --verbose
```

## Output

### Generated Files
- **Text Output**: Simple list of discovered email addresses
- **CSV Output**: Structured data with TheHarvester source information
- **JSON Output**: Detailed information including discovery metadata

### Report Contents
- **Email Addresses**: All discovered and validated email addresses
- **Discovery Sources**: Which TheHarvester modules found each email
- **Statistics**: Total modules used, emails found, processing time
- **Tool Output**: Raw TheHarvester output for reference

## Configuration

### Default Settings
- **Output Format**: Text format
- **Verbose Mode**: Off by default
- **TheHarvester Path**: Auto-detected
- **Timeout**: 300 seconds per domain

### Customization
- Specify custom TheHarvester installation path
- Configure output formats for different use cases
- Adjust timeout values for slow networks
- Customize email validation patterns

## Security Considerations

### Legal Notice
This tool is intended for authorized security testing only. Users must:
- Obtain proper authorization before searching for email addresses
- Comply with all applicable laws and regulations
- Respect rate limits and usage policies
- Use responsibly and ethically

### Best Practices
- Always obtain proper authorization before use
- Respect TheHarvester's terms of service
- Use appropriate delays between queries
- Follow responsible disclosure practices

## Troubleshooting

### Common Issues

1. **TheHarvester Not Found**
   ```
   Error: TheHarvester tool not found
   ```
   **Solution**: Install TheHarvester or specify correct path
   ```bash
   python3 theharvester_checker.py domain --theharvester-path /path/to/theHarvester
   ```

2. **No Results Found**
   ```
   Warning: No email addresses found
   ```
   **Solution**: Check domain spelling or try different domains

3. **Tool Execution Failed**
   ```
   Error: TheHarvester execution failed
   ```
   **Solution**: Check TheHarvester installation and dependencies

## Performance

### Optimization Tips
- Ensure TheHarvester is properly installed
- Use appropriate timeout values
- Monitor tool execution and output
- Consider using batch processing for multiple domains

### Resource Usage
- **Memory**: ~100-300MB (depends on TheHarvester)
- **CPU**: Moderate usage during tool execution
- **Network**: High bandwidth usage for comprehensive searches
- **Storage**: Minimal, only for output files

## Integration

### Script Integration
```python
import subprocess
import json

# Run TheHarvester checker
result = subprocess.run([
    'python3', 'theharvester_checker.py', 
    'example.com',
    '--format', 'json',
    '--output', 'theharvester_emails.json'
], capture_output=True, text=True)

# Parse results
with open('theharvester_emails.json', 'r') as f:
    data = json.load(f)
    
print(f"Found {len(data['emails'])} email addresses")
```

## Examples

### Comprehensive Email Discovery
```bash
#!/bin/bash
# Comprehensive email discovery using TheHarvester

DOMAIN="example.com"
OUTPUT_DIR="./theharvester_results"

python3 theharvester_checker.py "$DOMAIN" \
    --format json \
    --output "$OUTPUT_DIR/${DOMAIN}_theharvester.json" \
    --verbose
```

### Batch Domain Processing
```bash
#!/bin/bash
# Process multiple domains

DOMAINS=("example.com" "google.com" "github.com")
OUTPUT_DIR="./batch_theharvester_results"

for domain in "${DOMAINS[@]}"; do
    echo "Using TheHarvester for $domain..."
    python3 theharvester_checker.py "$domain" \
        --output "$OUTPUT_DIR/${domain}_theharvester.txt" \
        --format txt
done
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**
