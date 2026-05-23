# Search Engine Email Checker and Extractor

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The Search Engine Email Checker (`search_email_checker.py`) is a powerful tool that searches for email addresses related to a domain using multiple search engines. It provides comprehensive email discovery capabilities through Google, DuckDuckGo, and Yahoo search results.

## Features

### Core Capabilities
- **Multi-Search Engine Support**: Searches Google, DuckDuckGo, and Yahoo
- **Advanced Email Pattern Matching**: Uses sophisticated regex patterns to find email addresses
- **Email Validation**: Validates extracted email addresses for proper format
- **Deduplication**: Removes duplicate email addresses automatically
- **Rate Limiting**: Respectful searching with configurable delays
- **Multiple Output Formats**: Supports text, CSV, and JSON output formats

### Advanced Features
- **Engine Selection**: Choose specific search engines to use
- **Batch Processing**: Processes multiple domains in a single run
- **Error Handling**: Robust error handling with detailed logging
- **Statistics Reporting**: Comprehensive statistics on discovered emails
- **Professional Output**: Clean, organized output formatting

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
python3 search_email_checker.py <domain>
```

### Advanced Usage
```bash
python3 search_email_checker.py <domain> [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output file path | auto-generated |
| `--format` | Output format (txt, csv, json) | txt |
| `--engines` | Search engines to use (google,duckduckgo,yahoo) | all |
| `--batch` | Batch file with multiple domains | None |
| `--delay` | Delay between requests (seconds) | 2 |
| `--verbose` | Verbose output | False |

## Examples

### Single Domain Search
```bash
python3 search_email_checker.py example.com
```

### Specific Search Engines
```bash
python3 search_email_checker.py example.com --engines google,duckduckgo
```

### Custom Output Format
```bash
python3 search_email_checker.py example.com --format json --output search_emails.json
```

### Batch Processing
```bash
python3 search_email_checker.py --batch domains.txt --format csv
```

### Advanced Configuration
```bash
python3 search_email_checker.py example.com --engines google --delay 3 --verbose
```

## Output

### Generated Files
- **Text Output**: Simple list of discovered email addresses
- **CSV Output**: Structured data with search engine source information
- **JSON Output**: Detailed information including search results and metadata

### Report Contents
- **Email Addresses**: All discovered and validated email addresses
- **Search Engine Sources**: Which search engine found each email
- **Search Queries**: Queries used to find emails
- **Statistics**: Total searches performed, emails found, processing time

## Configuration

### Default Settings
- **Search Engines**: All available engines (Google, DuckDuckGo, Yahoo)
- **Request Delay**: 2 seconds between requests
- **Output Format**: Text format
- **Verbose Mode**: Off by default

### Customization
- Select specific search engines for targeted searches
- Adjust delays to respect search engine rate limits
- Configure output formats for different use cases
- Customize search queries and patterns

## Security Considerations

### Legal Notice
This tool is intended for authorized security testing only. Users must:
- Obtain proper authorization before searching for email addresses
- Comply with search engine terms of service
- Respect rate limits and usage policies
- Use responsibly and ethically

### Best Practices
- Always obtain proper authorization before use
- Respect search engine rate limits and terms of service
- Use appropriate delays between requests
- Follow responsible disclosure practices

## Troubleshooting

### Common Issues

1. **Search Engine Blocking**
   ```
   Error: Search engine blocked requests
   ```
   **Solution**: Increase delay between requests or use different engines

2. **No Results Found**
   ```
   Warning: No email addresses found
   ```
   **Solution**: Try different search engines or modify search queries

3. **Rate Limiting**
   ```
   Error: Too many requests
   ```
   **Solution**: Increase delay between requests

## Performance

### Optimization Tips
- Use appropriate delays to avoid rate limiting
- Select specific search engines for faster results
- Monitor search engine responses
- Consider using proxies for high-volume searches

### Resource Usage
- **Memory**: ~50-100MB
- **CPU**: Low to moderate usage during searches
- **Network**: Moderate bandwidth usage
- **Storage**: Minimal, only for output files

## Integration

### Script Integration
```python
import subprocess
import json

# Run search email checker
result = subprocess.run([
    'python3', 'search_email_checker.py', 
    'example.com',
    '--format', 'json',
    '--output', 'search_emails.json'
], capture_output=True, text=True)

# Parse results
with open('search_emails.json', 'r') as f:
    data = json.load(f)
    
print(f"Found {len(data['emails'])} email addresses")
```

## Examples

### Multi-Engine Search
```bash
#!/bin/bash
# Search multiple engines for emails

DOMAIN="example.com"
OUTPUT_DIR="./search_results"

python3 search_email_checker.py "$DOMAIN" \
    --engines google,duckduckgo,yahoo \
    --format json \
    --output "$OUTPUT_DIR/${DOMAIN}_search.json" \
    --verbose
```

### Batch Domain Search
```bash
#!/bin/bash
# Process multiple domains

DOMAINS=("example.com" "google.com" "github.com")
OUTPUT_DIR="./batch_search_results"

for domain in "${DOMAINS[@]}"; do
    echo "Searching for emails related to $domain..."
    python3 search_email_checker.py "$domain" \
        --output "$OUTPUT_DIR/${domain}_search.txt" \
        --format txt
done
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**
