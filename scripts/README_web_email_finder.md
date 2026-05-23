# Web Email Finder

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The Web Email Finder (`web_email_finder.py`) is a reliable tool that finds email addresses by scraping websites and searching for email patterns. It serves as a dependable alternative to tools that may have installation or runtime issues.

## Features

### Core Capabilities
- **Website Scraping**: Scrapes websites for email addresses using multiple methods
- **Pattern Matching**: Searches for common email patterns on websites
- **Email Extraction**: Extracts and validates email addresses
- **Deduplication**: Removes duplicate email addresses automatically
- **Multiple Output Formats**: Supports text, CSV, and JSON output formats
- **Reliable Operation**: Designed for consistent, reliable operation

### Advanced Features
- **Multiple Scraping Methods**: Uses various techniques to find emails
- **Batch Processing**: Processes multiple domains in a single run
- **Error Handling**: Robust error handling with detailed logging
- **Statistics Reporting**: Comprehensive statistics on discovered emails
- **Website Analysis**: Provides additional website information

## Installation

### Prerequisites
- Python 3.6 or higher
- Internet connectivity
- Required Python packages

### Dependencies
```bash
pip install requests beautifulsoup4 lxml
```

## Usage

### Basic Usage
```bash
python3 web_email_finder.py <domain>
```

### Advanced Usage
```bash
python3 web_email_finder.py <domain> [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output file path | auto-generated |
| `--format` | Output format (txt, csv, json) | txt |
| `--batch` | Batch file with multiple domains | None |
| `--verbose` | Verbose output | False |
| `--max-pages` | Maximum pages to scrape | 50 |

## Examples

### Single Domain Search
```bash
python3 web_email_finder.py example.com
```

### Custom Output Format
```bash
python3 web_email_finder.py example.com --format json --output web_emails.json
```

### Batch Processing
```bash
python3 web_email_finder.py --batch domains.txt --format csv
```

### Advanced Configuration
```bash
python3 web_email_finder.py example.com --max-pages 100 --verbose
```

## Output

### Generated Files
- **Text Output**: Simple list of discovered email addresses
- **CSV Output**: Structured data with website source information
- **JSON Output**: Detailed information including scraping metadata

### Report Contents
- **Email Addresses**: All discovered and validated email addresses
- **Source URLs**: URLs where each email was found
- **Scraping Statistics**: Total pages scraped, emails found, processing time
- **Website Analysis**: Additional website information and metadata

## Configuration

### Default Settings
- **Output Format**: Text format
- **Max Pages**: 50 pages per domain
- **Verbose Mode**: Off by default
- **Timeout**: 30 seconds per request

### Customization
- Configure maximum pages for large websites
- Adjust output formats for different use cases
- Modify timeout values for slow networks
- Customize email validation patterns

## Security Considerations

### Legal Notice
This tool is intended for authorized security testing only. Users must:
- Obtain proper authorization before scraping websites
- Comply with website terms of service and robots.txt
- Respect rate limits and server resources
- Use responsibly and ethically

### Best Practices
- Always check robots.txt before scraping
- Use appropriate delays to avoid overwhelming servers
- Respect website terms of service
- Only scrape websites you own or have permission to test

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   ```
   Error: Connection timeout
   ```
   **Solution**: Increase timeout or check network connectivity

2. **Rate Limiting**
   ```
   Error: Too many requests
   ```
   **Solution**: Add delays between requests

3. **Permission Denied**
   ```
   Error: 403 Forbidden
   ```
   **Solution**: Check robots.txt and website access policies

## Performance

### Optimization Tips
- Use appropriate delays to avoid rate limiting
- Configure maximum pages for large websites
- Monitor memory usage for extensive scraping
- Consider using proxies for high-volume scraping

### Resource Usage
- **Memory**: ~50-200MB depending on scraping scope
- **CPU**: Moderate usage during active scraping
- **Network**: High bandwidth usage for large websites
- **Storage**: Minimal, only for output files

## Integration

### Script Integration
```python
import subprocess
import json

# Run web email finder
result = subprocess.run([
    'python3', 'web_email_finder.py', 
    'example.com',
    '--format', 'json',
    '--output', 'web_emails.json'
], capture_output=True, text=True)

# Parse results
with open('web_emails.json', 'r') as f:
    data = json.load(f)
    
print(f"Found {len(data['emails'])} email addresses")
```

## Examples

### Website Email Discovery
```bash
#!/bin/bash
# Discover emails from website scraping

DOMAIN="example.com"
OUTPUT_DIR="./web_results"

python3 web_email_finder.py "$DOMAIN" \
    --format json \
    --output "$OUTPUT_DIR/${DOMAIN}_web.json" \
    --max-pages 100 \
    --verbose
```

### Batch Website Processing
```bash
#!/bin/bash
# Process multiple websites

DOMAINS=("example.com" "google.com" "github.com")
OUTPUT_DIR="./batch_web_results"

for domain in "${DOMAINS[@]}"; do
    echo "Scraping emails from $domain..."
    python3 web_email_finder.py "$domain" \
        --output "$OUTPUT_DIR/${domain}_web.txt" \
        --format txt \
        --max-pages 50
done
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**
