# EmailHarvester Email Checker

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The EmailHarvester Email Checker (`emailharvester_checker.py`) is a specialized tool that uses EmailHarvester to find email addresses associated with a domain. It leverages EmailHarvester's powerful email discovery capabilities for comprehensive email enumeration.

## Features

### Core Capabilities
- **EmailHarvester Integration**: Uses EmailHarvester tool for email discovery
- **Email Extraction**: Extracts email addresses from EmailHarvester output
- **Email Validation**: Validates extracted email addresses for proper format
- **Deduplication**: Removes duplicate email addresses automatically
- **Multiple Output Formats**: Supports text, CSV, and JSON output formats
- **Comprehensive Reporting**: Detailed statistics and analysis

### Advanced Features
- **Batch Processing**: Processes multiple domains in a single run
- **Error Handling**: Robust error handling with detailed logging
- **Statistics Reporting**: Comprehensive statistics on discovered emails
- **Tool Integration**: Seamless integration with EmailHarvester
- **Output Processing**: Advanced processing of EmailHarvester results

## Installation

### Prerequisites
- Python 3.6 or higher
- EmailHarvester tool installed
- Internet connectivity

### Dependencies
```bash
# Install EmailHarvester
git clone https://github.com/maldevel/EmailHarvester.git
cd EmailHarvester
pip install -r requirements.txt

# Python dependencies
pip install requests
```

## Usage

### Basic Usage
```bash
python3 emailharvester_checker.py <domain>
```

### Advanced Usage
```bash
python3 emailharvester_checker.py <domain> [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output file path | auto-generated |
| `--format` | Output format (txt, csv, json) | txt |
| `--batch` | Batch file with multiple domains | None |
| `--verbose` | Verbose output | False |
| `--emailharvester-path` | Path to EmailHarvester tool | auto-detect |

## Examples

### Single Domain Search
```bash
python3 emailharvester_checker.py example.com
```

### Custom Output Format
```bash
python3 emailharvester_checker.py example.com --format json --output emailharvester_emails.json
```

### Batch Processing
```bash
python3 emailharvester_checker.py --batch domains.txt --format csv
```

### Advanced Configuration
```bash
python3 emailharvester_checker.py example.com --emailharvester-path /path/to/EmailHarvester --verbose
```

## Output

### Generated Files
- **Text Output**: Simple list of discovered email addresses
- **CSV Output**: Structured data with EmailHarvester source information
- **JSON Output**: Detailed information including discovery metadata

### Report Contents
- **Email Addresses**: All discovered and validated email addresses
- **Discovery Sources**: Which EmailHarvester modules found each email
- **Statistics**: Total modules used, emails found, processing time
- **Tool Output**: Raw EmailHarvester output for reference

## Configuration

### Default Settings
- **Output Format**: Text format
- **Verbose Mode**: Off by default
- **EmailHarvester Path**: Auto-detected
- **Timeout**: 300 seconds per domain

### Customization
- Specify custom EmailHarvester installation path
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
- Respect EmailHarvester's terms of service
- Use appropriate delays between queries
- Follow responsible disclosure practices

## Troubleshooting

### Common Issues

1. **EmailHarvester Not Found**
   ```
   Error: EmailHarvester tool not found
   ```
   **Solution**: Install EmailHarvester or specify correct path
   ```bash
   python3 emailharvester_checker.py domain --emailharvester-path /path/to/EmailHarvester
   ```

2. **No Results Found**
   ```
   Warning: No email addresses found
   ```
   **Solution**: Check domain spelling or try different domains

3. **Tool Execution Failed**
   ```
   Error: EmailHarvester execution failed
   ```
   **Solution**: Check EmailHarvester installation and dependencies

## Performance

### Optimization Tips
- Ensure EmailHarvester is properly installed
- Use appropriate timeout values
- Monitor tool execution and output
- Consider using batch processing for multiple domains

### Resource Usage
- **Memory**: ~100-300MB (depends on EmailHarvester)
- **CPU**: Moderate usage during tool execution
- **Network**: High bandwidth usage for comprehensive searches
- **Storage**: Minimal, only for output files

## Integration

### Script Integration
```python
import subprocess
import json

# Run EmailHarvester checker
result = subprocess.run([
    'python3', 'emailharvester_checker.py', 
    'example.com',
    '--format', 'json',
    '--output', 'emailharvester_emails.json'
], capture_output=True, text=True)

# Parse results
with open('emailharvester_emails.json', 'r') as f:
    data = json.load(f)
    
print(f"Found {len(data['emails'])} email addresses")
```

## Examples

### Comprehensive Email Discovery
```bash
#!/bin/bash
# Comprehensive email discovery using EmailHarvester

DOMAIN="example.com"
OUTPUT_DIR="./emailharvester_results"

python3 emailharvester_checker.py "$DOMAIN" \
    --format json \
    --output "$OUTPUT_DIR/${DOMAIN}_emailharvester.json" \
    --verbose
```

### Batch Domain Processing
```bash
#!/bin/bash
# Process multiple domains

DOMAINS=("example.com" "google.com" "github.com")
OUTPUT_DIR="./batch_emailharvester_results"

for domain in "${DOMAINS[@]}"; do
    echo "Using EmailHarvester for $domain..."
    python3 emailharvester_checker.py "$domain" \
        --output "$OUTPUT_DIR/${domain}_emailharvester.txt" \
        --format txt
done
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**
