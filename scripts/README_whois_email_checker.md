# Whois Email Checker and Extractor

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The Whois Email Checker (`whois_email_checker.py`) is a specialized tool designed to extract email addresses from whois data for domains. It provides comprehensive email discovery capabilities for legitimate security assessments, contact information gathering, and compliance checking.

## Features

### Core Capabilities
- **Whois Query Execution**: Performs whois queries for specified domains
- **IP Resolution**: Resolves domain names to IP addresses and performs whois on IPs
- **Advanced Email Extraction**: Uses sophisticated regex patterns to find email addresses
- **Email Validation**: Validates extracted email addresses for proper format
- **Deduplication**: Removes duplicate email addresses automatically
- **Multiple Output Formats**: Supports text, CSV, and JSON output formats

### Advanced Features
- **Batch Processing**: Processes multiple domains in a single run
- **Error Handling**: Robust error handling with detailed logging
- **Statistics Reporting**: Comprehensive statistics on discovered emails
- **Domain Analysis**: Provides additional domain information
- **Contact Information**: Extracts various contact details from whois data

## Installation

### Prerequisites
- Python 3.6 or higher
- Internet connectivity
- whois command-line tool

### Dependencies
```bash
# Install whois tool
sudo apt install whois

# Python dependencies
pip install requests
```

## Usage

### Basic Usage
```bash
python3 whois_email_checker.py <domain>
```

### Advanced Usage
```bash
python3 whois_email_checker.py <domain> [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output file path | auto-generated |
| `--format` | Output format (txt, csv, json) | txt |
| `--batch` | Batch file with multiple domains | None |
| `--verbose` | Verbose output | False |
| `--include-ips` | Include IP whois data | False |

## Examples

### Single Domain
```bash
python3 whois_email_checker.py example.com
```

### Multiple Domains
```bash
python3 whois_email_checker.py example.com google.com github.com
```

### Batch Processing
```bash
python3 whois_email_checker.py --batch domains.txt --format json
```

### Advanced Configuration
```bash
python3 whois_email_checker.py example.com --include-ips --format csv --output whois_emails.csv
```

## Output

### Generated Files
- **Text Output**: Simple list of discovered email addresses
- **CSV Output**: Structured data with domain and contact information
- **JSON Output**: Detailed information including whois data and metadata

### Report Contents
- **Email Addresses**: All discovered and validated email addresses
- **Domain Information**: Domain registration details
- **Contact Information**: Administrative and technical contacts
- **Statistics**: Total domains processed, emails found, processing time

## Configuration

### Default Settings
- **Output Format**: Text format
- **Include IPs**: Disabled by default
- **Verbose Mode**: Off by default
- **Timeout**: 30 seconds per whois query

### Customization
- Enable IP whois for additional email discovery
- Configure output formats for different use cases
- Adjust timeout values for slow networks
- Customize email validation patterns

## Security Considerations

### Legal Notice
This tool is intended for authorized security testing only. Users must:
- Obtain proper authorization before querying whois data
- Comply with all applicable laws and regulations
- Respect whois server rate limits
- Use responsibly and ethically

### Best Practices
- Always obtain proper authorization before use
- Respect whois server rate limits
- Use appropriate delays between queries
- Follow responsible disclosure practices

## Troubleshooting

### Common Issues

1. **Whois Command Not Found**
   ```
   Error: whois command not found
   ```
   **Solution**: Install whois tool
   ```bash
   sudo apt install whois
   ```

2. **Query Timeout**
   ```
   Error: Whois query timed out
   ```
   **Solution**: Check network connectivity or increase timeout

3. **Rate Limiting**
   ```
   Error: Too many requests
   ```
   **Solution**: Add delays between queries

## Performance

### Optimization Tips
- Use batch processing for multiple domains
- Add appropriate delays between queries
- Monitor whois server responses
- Consider using multiple whois servers

### Resource Usage
- **Memory**: ~10-50MB
- **CPU**: Low usage during queries
- **Network**: Moderate bandwidth usage
- **Storage**: Minimal, only for output files

## Integration

### Script Integration
```python
import subprocess
import json

# Run whois email checker
result = subprocess.run([
    'python3', 'whois_email_checker.py', 
    'example.com',
    '--format', 'json',
    '--output', 'whois_emails.json'
], capture_output=True, text=True)

# Parse results
with open('whois_emails.json', 'r') as f:
    data = json.load(f)
    
print(f"Found {len(data['emails'])} email addresses")
```

## Examples

### Domain Investigation
```bash
#!/bin/bash
# Investigate multiple domains

DOMAINS=("example.com" "google.com" "github.com")
OUTPUT_DIR="./whois_results"

for domain in "${DOMAINS[@]}"; do
    echo "Checking whois for $domain..."
    python3 whois_email_checker.py "$domain" \
        --output "$OUTPUT_DIR/${domain}_whois.txt" \
        --format txt
done
```

### Batch Processing
```bash
#!/bin/bash
# Process domains from file

python3 whois_email_checker.py \
    --batch domains.txt \
    --format json \
    --output all_whois_emails.json \
    --verbose
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**
