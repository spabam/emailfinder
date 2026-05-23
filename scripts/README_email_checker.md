# Email Checker and Web Crawler

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The Email Checker (`email_checker.py`) is a comprehensive web crawler designed to extract email addresses from websites. It provides advanced email discovery capabilities for legitimate security assessments, contact information gathering, and compliance checking.

## Features

### Core Capabilities
- **Multi-threaded Web Crawling**: Efficient crawling of websites with configurable thread count
- **Advanced Email Extraction**: Uses sophisticated regex patterns to find email addresses
- **Link Following**: Automatically follows internal links to discover all pages
- **Email Validation**: Validates extracted email addresses for proper format
- **Deduplication**: Removes duplicate email addresses automatically
- **Multiple Output Formats**: Supports text, CSV, and JSON output formats

### Advanced Features
- **Rate Limiting**: Configurable delays to respect server resources
- **User Agent Rotation**: Uses different user agents to avoid detection
- **Error Handling**: Robust error handling with detailed logging
- **Progress Tracking**: Real-time progress updates during crawling
- **Statistics Reporting**: Comprehensive statistics on discovered emails

## Installation

### Prerequisites
- Python 3.6 or higher
- Internet connectivity
- Required Python packages (see requirements.txt)

### Dependencies
```bash
pip install requests beautifulsoup4 lxml
```

## Usage

### Basic Usage
```bash
python3 email_checker.py <target_url>
```

### Advanced Usage
```bash
python3 email_checker.py <target_url> [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output file path | auto-generated |
| `--format` | Output format (txt, csv, json) | txt |
| `--threads` | Number of threads | 5 |
| `--delay` | Delay between requests (seconds) | 1 |
| `--max-pages` | Maximum pages to crawl | 100 |
| `--verbose` | Verbose output | False |

## Examples

### Basic Web Crawling
```bash
python3 email_checker.py https://example.com
```

### Advanced Configuration
```bash
python3 email_checker.py https://example.com --threads 10 --delay 0.5 --format json --output emails.json
```

### Large Site Crawling
```bash
python3 email_checker.py https://large-site.com --max-pages 500 --threads 15 --verbose
```

## Output

### Generated Files
- **Text Output**: Simple list of discovered email addresses
- **CSV Output**: Structured data with additional metadata
- **JSON Output**: Detailed information including source URLs and timestamps

### Report Contents
- **Email Addresses**: All discovered and validated email addresses
- **Source URLs**: URLs where each email was found
- **Statistics**: Total pages crawled, emails found, processing time
- **Validation Results**: Information about email validation

## Configuration

### Default Settings
- **Thread Count**: 5 concurrent threads
- **Request Delay**: 1 second between requests
- **Max Pages**: 100 pages per crawl
- **User Agent**: Rotating user agents
- **Timeout**: 30 seconds per request

### Customization
- Modify thread count for performance tuning
- Adjust delays to respect server resources
- Configure maximum pages for large sites
- Customize user agents and headers

## Security Considerations

### Legal Notice
This tool is intended for authorized security testing only. Users must:
- Obtain proper authorization before crawling websites
- Comply with robots.txt and website terms of service
- Respect rate limits and server resources
- Use responsibly and ethically

### Best Practices
- Always check robots.txt before crawling
- Use appropriate delays to avoid overwhelming servers
- Respect website terms of service
- Only crawl websites you own or have permission to test

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
   **Solution**: Increase delay between requests

3. **Permission Denied**
   ```
   Error: 403 Forbidden
   ```
   **Solution**: Check robots.txt and website access policies

## Performance

### Optimization Tips
- Adjust thread count based on target server capacity
- Use appropriate delays to avoid rate limiting
- Monitor memory usage for large crawls
- Consider using proxies for high-volume crawling

### Resource Usage
- **Memory**: ~50-200MB depending on crawl size
- **CPU**: Moderate usage during active crawling
- **Network**: High bandwidth usage for large sites
- **Storage**: Minimal, only for output files

## Integration

### Script Integration
```python
import subprocess
import json

# Run email checker
result = subprocess.run([
    'python3', 'email_checker.py', 
    'https://example.com',
    '--format', 'json',
    '--output', 'emails.json'
], capture_output=True, text=True)

# Parse results
with open('emails.json', 'r') as f:
    data = json.load(f)
    
print(f"Found {len(data['emails'])} email addresses")
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**
