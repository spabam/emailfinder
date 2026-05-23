# Search Engine Email Checker and Extractor

A comprehensive tool for searching email addresses related to a domain using multiple search engines (Google, DuckDuckGo, Yahoo). This tool provides powerful email discovery capabilities for legitimate security assessments, contact information gathering, and compliance checking.

## Features

- **Multi-Search Engine Support**: Searches Google, DuckDuckGo, and Yahoo simultaneously
- **Advanced Email Detection**: Multiple regex patterns to find various email formats in search results
- **Intelligent Validation**: Email address validation and deduplication
- **Rate Limiting**: Respectful delays between requests to avoid being blocked
- **Comprehensive Reporting**: Detailed statistics and progress tracking
- **Multiple Export Formats**: Text, CSV, and JSON output options
- **Error Handling**: Graceful handling of search engine failures and timeouts

## Email Pattern Detection

The checker can detect emails in various formats from search results:
- Standard email addresses: `user@domain.com`
- Obfuscated emails: `user[at]domain[dot]com`
- JavaScript emails: `"user@domain.com"`
- Mailto links: `mailto:user@domain.com`
- Search result content: Emails found in web page content

## Installation

### Quick Setup

1. Run the setup script:
```bash
./setup_search.sh
```

2. Use the run script:
```bash
./run_search_email_checker.sh example.com
```

### Manual Setup

1. Create virtual environment:
```bash
python3 -m venv $HOME/search_email_checker_env
```

2. Activate environment:
```bash
source $HOME/search_email_checker_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Basic search engine email extraction
python3 search_email_checker.py example.com

# Multiple domains
python3 search_email_checker.py example.com google.com github.com

# With output file
python3 search_email_checker.py example.com --output emails.txt
```

### Advanced Options

```bash
# Export in different formats
python3 search_email_checker.py example.com --output results.json --format json
python3 search_email_checker.py example.com --output results.csv --format csv

# Use specific search engines
python3 search_email_checker.py example.com --engines google,duckduckgo

# Custom delay and timeout
python3 search_email_checker.py example.com --delay 3.0 --timeout 15

# Verbose logging
python3 search_email_checker.py example.com --verbose
```

### Using the Run Script

```bash
# Basic search
./run_search_email_checker.sh example.com

# Multiple domains
./run_search_email_checker.sh example.com google.com github.com

# With options
./run_search_email_checker.sh example.com --output emails.txt

# Specific engines
./run_search_email_checker.sh example.com --engines google,duckduckgo

# Show banner
./run_search_email_checker.sh --banner
```

## Examples

### Basic Email Discovery

```bash
$ python3 search_email_checker.py microsoft.com
🔍 Starting search engine email extraction
📋 Domains: microsoft.com
============================================================

📊 SEARCH RESULTS:
   Domains searched: 1
   Emails found: 2
   Unique emails: 2
   Errors: 0
   Duration: 0:00:06.441943
============================================================

📧 EMAIL ADDRESSES FOUND (2):
----------------------------------------
   1. satyan@microsoft.com
   2. wehelp@microsoft.com
```

### Multiple Domains

```bash
$ python3 search_email_checker.py microsoft.com google.com
🔍 Starting search engine email extraction
📋 Domains: microsoft.com, google.com
============================================================

📊 SEARCH RESULTS:
   Domains searched: 2
   Emails found: 3
   Unique emails: 3
   Errors: 0
   Duration: 0:00:12.883886
============================================================

📧 EMAIL ADDRESSES FOUND (3):
----------------------------------------
   1. satyan@microsoft.com
   2. wehelp@microsoft.com
   3. support@google.com
```

### Export to File

```bash
$ python3 search_email_checker.py microsoft.com --output search_emails.txt
# Results saved to search_emails.txt with detailed breakdown
```

### CSV Export

```bash
$ python3 search_email_checker.py microsoft.com --output results.csv --format csv
# Creates CSV with columns: Email, Domain, Email_Domain
```

## Command Line Options

- `domains`: Domain(s) to search for email addresses (required)
- `--output, -o`: Output file path
- `--format`: Output format (txt, csv, json)
- `--engines`: Comma-separated list of search engines (default: google,duckduckgo,yahoo)
- `--delay`: Delay between requests in seconds (default: 2.0)
- `--timeout`: Request timeout in seconds (default: 10)
- `--verbose, -v`: Enable verbose logging
- `--banner`: Show tool banner and exit

## Supported Search Engines

- **Google**: Primary search engine with comprehensive results
- **DuckDuckGo**: Privacy-focused search engine
- **Yahoo**: Alternative search engine for additional coverage

## Output Formats

### Text Format
```
Search Engine Email Checker Results
===================================

Domains Searched: 1
Emails Found: 2
Unique Emails: 2
Errors: 0
Duration: 0:00:06.441943

All Email Addresses Found:
------------------------------
satyan@microsoft.com
wehelp@microsoft.com

Emails by Domain:
------------------------------

microsoft.com:
  satyan@microsoft.com
  wehelp@microsoft.com
```

### CSV Format
```csv
Email,Domain,Email_Domain
satyan@microsoft.com,microsoft.com,microsoft.com
wehelp@microsoft.com,microsoft.com,microsoft.com
```

### JSON Format
```json
{
  "domains": [
    {
      "domain": "microsoft.com",
      "emails": ["satyan@microsoft.com", "wehelp@microsoft.com"],
      "search_results": {
        "google": {
          "engine": "google",
          "engine_name": "Google",
          "emails": ["wehelp@microsoft.com"],
          "results_processed": 20,
          "error": null
        },
        "duckduckgo": {
          "engine": "duckduckgo",
          "engine_name": "DuckDuckGo",
          "emails": ["satyan@microsoft.com"],
          "results_processed": 20,
          "error": null
        }
      },
      "error": null
    }
  ],
  "all_emails": ["satyan@microsoft.com", "wehelp@microsoft.com"],
  "domain_emails": {
    "microsoft.com": ["satyan@microsoft.com", "wehelp@microsoft.com"]
  },
  "stats": {
    "domains_searched": 1,
    "emails_found": 2,
    "unique_emails": 2,
    "errors": 0,
    "start_time": "2025-10-13 01:52:03.794000",
    "end_time": "2025-10-13 01:52:03.946000"
  }
}
```

## Security Considerations

- **Legitimate Use Only**: This tool is designed for legitimate security assessments and research
- **Authorization Required**: Always obtain proper authorization before testing
- **Respectful Searching**: Implements rate limiting to avoid being blocked
- **Public Information Only**: Only searches for publicly available information
- **Legal Compliance**: Use in accordance with applicable laws and regulations

## Use Cases

- **Security Assessments**: Email discovery for penetration testing
- **Contact Information Gathering**: Finding contact details for legitimate purposes
- **Compliance Checking**: Verifying email address exposure in public sources
- **Domain Analysis**: Analyzing publicly available email addresses
- **Data Discovery**: Inventory of email addresses from search engines

## Requirements

- Python 3.6+
- requests library
- beautifulsoup4 library
- urllib3 library
- lxml library
- Internet connection

## Performance Tips

- **Rate Limiting**: Use appropriate delays to avoid being blocked by search engines
- **Search Engine Selection**: Choose specific engines for faster results
- **Timeout Settings**: Adjust timeout based on network conditions
- **Batch Processing**: Process multiple domains in a single command

## Limitations

- **Search Engine Policies**: Results may be limited by search engine anti-bot measures
- **Rate Limiting**: Must respect search engine rate limits to avoid blocking
- **Result Quality**: Search results may vary based on search engine algorithms
- **Network Dependency**: Requires stable internet connection

## License

This tool is provided as-is for educational and security assessment purposes.
Use responsibly and in accordance with applicable laws and regulations.

## Copyright

Copyright (c) 2025-2035 Andrea Bodei - info@andreabodei.com

