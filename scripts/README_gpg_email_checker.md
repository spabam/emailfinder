# GPG/PGP Email Checker

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The GPG/PGP Email Checker (`gpg_email_checker.py`) is a specialized tool that searches GPG/PGP key servers for email addresses associated with a domain. It provides comprehensive email discovery capabilities through multiple GPG key servers.

## Features

### Core Capabilities
- **Multi-Server Support**: Queries multiple GPG key servers
- **Email Extraction**: Extracts email addresses from GPG key data
- **Email Validation**: Validates extracted email addresses for proper format
- **Deduplication**: Removes duplicate email addresses automatically
- **Multiple Output Formats**: Supports text, CSV, and JSON output formats
- **Key Server Integration**: Connects to major GPG key servers

### Advanced Features
- **Server Selection**: Choose specific GPG key servers to query
- **Batch Processing**: Processes multiple domains in a single run
- **Error Handling**: Robust error handling with detailed logging
- **Statistics Reporting**: Comprehensive statistics on discovered emails
- **Key Information**: Provides additional GPG key metadata

## Installation

### Prerequisites
- Python 3.6 or higher
- Internet connectivity
- Required Python packages

### Dependencies
```bash
pip install requests
```

## Usage

### Basic Usage
```bash
python3 gpg_email_checker.py <domain>
```

### Advanced Usage
```bash
python3 gpg_email_checker.py <domain> [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output file path | auto-generated |
| `--format` | Output format (txt, csv, json) | txt |
| `--servers` | GPG servers to query | all available |
| `--batch` | Batch file with multiple domains | None |
| `--verbose` | Verbose output | False |

## Examples

### Single Domain Search
```bash
python3 gpg_email_checker.py example.com
```

### Specific GPG Servers
```bash
python3 gpg_email_checker.py example.com --servers keys.openpgp.org,pgp.mit.edu
```

### Custom Output Format
```bash
python3 gpg_email_checker.py example.com --format json --output gpg_emails.json
```

### Batch Processing
```bash
python3 gpg_email_checker.py --batch domains.txt --format csv
```

### Advanced Configuration
```bash
python3 gpg_email_checker.py example.com --servers keys.openpgp.org --verbose
```

## Output

### Generated Files
- **Text Output**: Simple list of discovered email addresses
- **CSV Output**: Structured data with GPG key information
- **JSON Output**: Detailed information including key metadata

### Report Contents
- **Email Addresses**: All discovered and validated email addresses
- **GPG Key Information**: Key IDs, creation dates, and other metadata
- **Server Sources**: Which GPG server found each email
- **Statistics**: Total servers queried, emails found, processing time

## Configuration

### Default Settings
- **GPG Servers**: All available servers (keys.openpgp.org, pgp.mit.edu, keyserver.ubuntu.com)
- **Output Format**: Text format
- **Verbose Mode**: Off by default
- **Timeout**: 30 seconds per server query

### Customization
- Select specific GPG servers for targeted searches
- Configure output formats for different use cases
- Adjust timeout values for slow networks
- Customize email validation patterns

## Security Considerations

### Legal Notice
This tool is intended for authorized security testing only. Users must:
- Obtain proper authorization before searching for email addresses
- Comply with GPG key server terms of service
- Respect server rate limits and usage policies
- Use responsibly and ethically

### Best Practices
- Always obtain proper authorization before use
- Respect GPG server rate limits
- Use appropriate delays between queries
- Follow responsible disclosure practices

## Troubleshooting

### Common Issues

1. **Server Connection Failed**
   ```
   Error: Failed to connect to GPG server
   ```
   **Solution**: Check network connectivity or try different servers

2. **No Results Found**
   ```
   Warning: No email addresses found
   ```
   **Solution**: Try different GPG servers or check domain spelling

3. **Rate Limiting**
   ```
   Error: Server rate limit exceeded
   ```
   **Solution**: Add delays between queries or use different servers

## Performance

### Optimization Tips
- Use appropriate delays to avoid rate limiting
- Select specific GPG servers for faster results
- Monitor server responses and availability
- Consider using multiple servers in parallel

### Resource Usage
- **Memory**: ~20-50MB
- **CPU**: Low usage during queries
- **Network**: Low to moderate bandwidth usage
- **Storage**: Minimal, only for output files

## Integration

### Script Integration
```python
import subprocess
import json

# Run GPG email checker
result = subprocess.run([
    'python3', 'gpg_email_checker.py', 
    'example.com',
    '--format', 'json',
    '--output', 'gpg_emails.json'
], capture_output=True, text=True)

# Parse results
with open('gpg_emails.json', 'r') as f:
    data = json.load(f)
    
print(f"Found {len(data['emails'])} email addresses")
```

## Examples

### Multi-Server Search
```bash
#!/bin/bash
# Search multiple GPG servers

DOMAIN="example.com"
OUTPUT_DIR="./gpg_results"

python3 gpg_email_checker.py "$DOMAIN" \
    --servers keys.openpgp.org,pgp.mit.edu,keyserver.ubuntu.com \
    --format json \
    --output "$OUTPUT_DIR/${DOMAIN}_gpg.json" \
    --verbose
```

### Batch Domain Search
```bash
#!/bin/bash
# Process multiple domains

DOMAINS=("example.com" "google.com" "github.com")
OUTPUT_DIR="./batch_gpg_results"

for domain in "${DOMAINS[@]}"; do
    echo "Searching GPG keys for $domain..."
    python3 gpg_email_checker.py "$domain" \
        --output "$OUTPUT_DIR/${domain}_gpg.txt" \
        --format txt
done
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**
