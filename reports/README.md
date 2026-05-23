# Email Finder Suite

A comprehensive suite of tools for discovering email addresses from multiple sources. This collection provides powerful email discovery capabilities for legitimate security assessments, contact information gathering, and compliance checking.

## Tools Included

### 1. Web Email Checker (`email_checker.py`)
Crawls websites and extracts email addresses from all pages using multi-threaded processing.

### 2. Whois Email Checker (`whois_email_checker.py`)
Extracts email addresses from whois data for domain registration information.

### 3. Search Engine Email Checker (`search_email_checker.py`)
Searches Google, DuckDuckGo, and Yahoo for email addresses related to a domain.

### 4. GPG/PGP Email Checker (`gpg_email_checker.py`)
Searches GPG key servers for email addresses associated with a domain.

### 5. EmailHarvester Email Checker (`emailharvester_checker.py`)
Uses EmailHarvester to find email addresses associated with a domain.

### 6. TheHarvester Email Checker (`theharvester_checker.py`)
Uses TheHarvester to find email addresses associated with a domain.

### 7. Comprehensive Email Finder (`run_enumeration.sh`)
Runs all email finding tools sequentially and merges their outputs into a single, ordered, unique list.

## Features

### Web Email Checker
- **Multi-threaded Crawling**: Concurrent page processing for improved performance
- **Advanced Email Detection**: Multiple regex patterns to find various email formats
- **Intelligent Validation**: Email address validation and deduplication
- **Domain Filtering**: Restrict crawling to specific domains
- **Respectful Crawling**: Rate limiting and robots.txt compliance
- **Multiple Export Formats**: Text, CSV, and JSON output options
- **Comprehensive Reporting**: Detailed statistics and progress tracking

### Whois Email Checker
- **Domain Registration Data**: Extracts emails from whois information
- **Multiple Domain Support**: Process single or multiple domains
- **Email Validation**: Validates and cleans email addresses
- **Duplicate Detection**: Automatically removes duplicate emails
- **Export Capabilities**: Text, CSV, and JSON output formats
- **Error Handling**: Graceful handling of whois failures

### Search Engine Email Checker
- **Multi-Engine Support**: Google, DuckDuckGo, and Yahoo search
- **Advanced Pattern Matching**: Finds emails in search results
- **Rate Limiting**: Respectful delays between requests
- **Email Validation**: Validates and cleans found emails
- **Duplicate Removal**: Automatically removes duplicate emails
- **Export Options**: Text, CSV, and JSON output formats

### GPG/PGP Email Checker
- **Multi-Server Support**: Searches keys.openpgp.org, pgp.mit.edu, and keyserver.ubuntu.com
- **Domain-Specific Search**: Finds emails associated with target domain
- **Common Pattern Search**: Searches for common email patterns (admin, contact, info, etc.)
- **Email Validation**: Validates and cleans found email addresses
- **Rate Limiting**: Respectful delays between server requests
- **Export Options**: Text, CSV, and JSON output formats
- **Comprehensive Reporting**: Detailed statistics and search results

### EmailHarvester Email Checker
- **EmailHarvester Integration**: Uses EmailHarvester tool for email discovery
- **Domain-Specific Search**: Finds emails associated with target domain
- **Email Validation**: Validates and cleans found email addresses
- **Error Handling**: Graceful handling of tool failures
- **Export Options**: Text, CSV, and JSON output formats
- **Comprehensive Reporting**: Detailed statistics and search results

### TheHarvester Email Checker
- **TheHarvester Integration**: Uses TheHarvester tool for email discovery
- **Multi-Engine Support**: Leverages TheHarvester's multiple search engines
- **Domain-Specific Search**: Finds emails associated with target domain
- **Email Validation**: Validates and cleans found email addresses
- **Error Handling**: Graceful handling of tool failures
- **Export Options**: Text, CSV, and JSON output formats
- **Comprehensive Reporting**: Detailed statistics and search results

### Comprehensive Email Finder
- **All-in-One Solution**: Runs all email finding tools
- **Intelligent Merging**: Combines results from all sources
- **Source Attribution**: Tracks which tool found each email
- **Deduplication**: Removes duplicates across all sources
- **Comprehensive Statistics**: Detailed reporting from all tools
- **Multiple Export Formats**: Text, CSV, and JSON with source tracking

## Email Pattern Detection

All tools can detect emails in various formats:
- Standard email addresses: `user@domain.com`
- Obfuscated emails: `user[at]domain[dot]com`
- JavaScript emails: `"user@domain.com"`
- Mailto links: `mailto:user@domain.com`
- Search result emails: Emails found in web search results

## Installation

### Quick Setup

1. **Web Email Checker**:
```bash
./installer.sh
```

2. **Whois Email Checker**:
```bash
./scripts/setup_whois.sh
```

3. **Search Engine Email Checker**:
```bash
./scripts/setup_search.sh
```

4. **GPG/PGP Email Checker**:
```bash
./scripts/setup_gpg.sh
```

5. **EmailHarvester Email Checker**:
```bash
./scripts/setup_emailharvester.sh
```

6. **TheHarvester Email Checker**:
```bash
./scripts/setup_theharvester.sh
```

### Manual Setup

Each tool has its own virtual environment:

```bash
# Web Email Checker
python3 -m venv /home/spabam/.venv
source /home/spabam/.venv/bin/activate
pip install -r requirements.txt

# Whois Email Checker
python3 -m venv /home/spabam/.venv
source /home/spabam/.venv/bin/activate
pip install -r requirements.txt

# Search Engine Email Checker
python3 -m venv /home/spabam/.venv
source /home/spabam/.venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Individual Tools

#### Web Email Checker
```bash
# Basic crawling
./scripts/run_email_checker.sh https://example.com

# With options
./scripts/run_email_checker.sh https://example.com --max-depth 3 --output emails.txt

# Show banner
./scripts/run_email_checker.sh --banner
```

#### Whois Email Checker
```bash
# Single domain
./scripts/run_whois_email_checker.sh example.com

# Multiple domains
./scripts/run_whois_email_checker.sh example.com google.com github.com

# With output
./scripts/run_whois_email_checker.sh example.com --output emails.txt

# Show banner
./scripts/run_whois_email_checker.sh --banner
```

#### Search Engine Email Checker
```bash
# Basic search
./scripts/run_search_email_checker.sh example.com

# Specific engines
./scripts/run_search_email_checker.sh example.com --engines google,duckduckgo

# With output
./scripts/run_search_email_checker.sh example.com --output emails.txt

# Show banner
./scripts/run_search_email_checker.sh --banner
```

#### GPG/PGP Email Checker
```bash
# Basic GPG search
./scripts/run_gpg_email_checker.sh example.com

# With output file
./scripts/run_gpg_email_checker.sh example.com --output emails.txt

# JSON output
./scripts/run_gpg_email_checker.sh example.com --output emails.json

# Verbose output
./scripts/run_gpg_email_checker.sh example.com --verbose

# Show banner
./scripts/run_gpg_email_checker.sh --banner
```

#### EmailHarvester Email Checker
```bash
# Basic EmailHarvester search
./scripts/run_emailharvester_checker.sh example.com

# With output file
./scripts/run_emailharvester_checker.sh example.com --output emails.txt

# JSON output
./scripts/run_emailharvester_checker.sh example.com --output emails.json

# Verbose output
./scripts/run_emailharvester_checker.sh example.com --verbose

# Show banner
./scripts/run_emailharvester_checker.sh --banner
```

#### TheHarvester Email Checker
```bash
# Basic TheHarvester search
./scripts/run_theharvester_checker.sh example.com

# With output file
./scripts/run_theharvester_checker.sh example.com --output emails.txt

# JSON output
./scripts/run_theharvester_checker.sh example.com --output emails.json

# Verbose output
./scripts/run_theharvester_checker.sh example.com --verbose

# Show banner
./scripts/run_theharvester_checker.sh --banner
```

### Comprehensive Email Finder

```bash
# Basic comprehensive search
./run_enumeration.sh example.com

# With options
./run_enumeration.sh example.com --output all_emails.txt

# CSV export with source tracking
./run_enumeration.sh example.com --output results.csv --format csv

# Custom search engines
./run_enumeration.sh example.com --engines google,duckduckgo

# Show banner
./run_enumeration.sh --banner
```

## Examples

### Comprehensive Email Discovery

```bash
$ ./run_enumeration.sh microsoft.com
╔══════════════════════════════════════════════════════════════════════════════╗
║                         Email Enumeration Runner                           ║
║  Copyright (c) 2025-2035 Andrea Bodei - info@andreabodei.com                ║
║  • Web Email Checker - Crawls websites for email addresses                  ║
║  • Whois Email Checker - Extracts emails from whois data                    ║
║  • Search Engine Email Checker - Searches Google, DuckDuckGo, Yahoo        ║
║  • Merged, deduplicated, and sorted output                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

🔍 Running Web Email Checker...
[SUCCESS] Web checker found 0 emails

🔍 Running Whois Email Checker...
[SUCCESS] Whois checker found 4 emails

🔍 Running Search Engine Email Checker...
[SUCCESS] Search checker found 2 emails

🔄 Merging and deduplicating emails...
[SUCCESS] Merged 6 emails into 6 unique emails

📊 FINAL RESULTS
============================================================
Target: microsoft.com
Web Emails Found: 0
Whois Emails Found: 4
Search Emails Found: 2
Total Emails: 6
Unique Emails: 6
Duration: 6s
============================================================

📧 EMAIL ADDRESSES FOUND (6):
----------------------------------------
  1. abusecomplaints@markmonitor.com
  2. admin@domains.microsoft
  3. msnhst@microsoft.com
  4. satyan@microsoft.com
  5. wehelp@microsoft.com
  6. whoisrequest@markmonitor.com
```

### CSV Export with Source Tracking

```bash
$ ./run_enumeration.sh example.com --output results.csv --format csv
$ cat results.csv
Email,Source,Target
abusecomplaints@markmonitor.com,Whois,example.com
admin@domains.microsoft,Whois,example.com
wehelp@microsoft.com,Search,example.com
```

## Command Line Options

### Comprehensive Email Finder Options
- `--output, -o`: Output file path (default: stdout)
- `--format`: Output format: txt, csv, json (default: txt)
- `--max-depth N`: Maximum crawling depth for web checker (default: 3)
- `--max-pages N`: Maximum pages to crawl (default: 20)
- `--threads N`: Number of threads for web crawling (default: 3)
- `--delay N`: Delay between requests in seconds (default: 1.0)
- `--engines ENGINES`: Comma-separated search engines (default: google,duckduckgo,yahoo)
- `--verbose, -v`: Enable verbose output (disables silent mode)
- `--debug`: Enable debug output (disables silent mode)
- `--silent`: Suppress progress output; show results only (default)
- Automatic retry: Each tool is re-run once if it exits with a non-zero code.
- `--help, -h`: Show help message
- `--banner`: Show tool banner and exit

### Individual Tool Options

#### Web Email Checker
- `--max-depth, -d`: Maximum crawling depth (default: 5)
- `--max-pages, -p`: Maximum number of pages to crawl (default: 100)
- `--threads, -t`: Number of threads for concurrent crawling (default: 3)
- `--delay`: Delay between requests in seconds (default: 1.0)
- `--domain`: Restrict crawling to specific domain
- `--output, -o`: Output file path
- `--format`: Output format (txt, csv, json)
- `--no-robots`: Do not respect robots.txt
- `--verbose, -v`: Enable verbose logging

#### Whois Email Checker
- `--output, -o`: Output file path
- `--format`: Output format (txt, csv, json)
- `--verbose, -v`: Enable verbose logging

#### Search Engine Email Checker
- `--output, -o`: Output file path
- `--format`: Output format (txt, csv, json)
- `--engines`: Comma-separated list of search engines
- `--delay`: Delay between requests in seconds (default: 2.0)
- `--timeout`: Request timeout in seconds (default: 10)
- `--verbose, -v`: Enable verbose logging

## Output Formats

### Text Format
```
Email Enumeration Results
=========================

Target: example.com
Web Emails Found: 2
Whois Emails Found: 4
Search Emails Found: 1
Total Emails: 7
Unique Emails: 6
Duration: 8s

Email Addresses Found:
----------------------
admin@example.com
contact@example.com
info@example.com
support@example.com
webmaster@example.com
```

### CSV Format with Source Tracking
```csv
Email,Source,Target
admin@example.com,Web,example.com
contact@example.com,Web,example.com
info@example.com,Whois,example.com
support@example.com,Whois,example.com
webmaster@example.com,Search,example.com
```

### JSON Format
```json
{
  "target": "example.com",
  "web_emails_found": 2,
  "whois_emails_found": 4,
  "search_emails_found": 1,
  "total_emails": 7,
  "unique_emails": 6,
  "duration_seconds": 8,
  "emails": [
    "admin@example.com",
    "contact@example.com",
    "info@example.com",
    "support@example.com",
    "webmaster@example.com"
  ]
}
```

## Security Considerations

- **Legitimate Use Only**: These tools are designed for legitimate security assessments and research
- **Authorization Required**: Always obtain proper authorization before testing
- **Respectful Operation**: Implements rate limiting and respects robots.txt
- **Public Content Only**: Only accesses publicly available content
- **Legal Compliance**: Use in accordance with applicable laws and regulations

## Use Cases

- **Security Assessments**: Comprehensive email discovery for penetration testing
- **Contact Information Gathering**: Finding contact details for legitimate purposes
- **Compliance Checking**: Verifying email address exposure across multiple sources
- **Website Auditing**: Analyzing email address distribution across sites
- **Data Discovery**: Inventory of email addresses from multiple sources
- **Domain Analysis**: Understanding email infrastructure and contact points

## Requirements

- Python 3.6+
- requests library
- beautifulsoup4 library
- urllib3 library
- lxml library
- whois command-line tool (for whois checker)
- Internet connection

## Performance Tips

- **Comprehensive Tool**: Use `run_enumeration.sh` for complete email discovery
- **Individual Tools**: Use specific tools for targeted searches
- **Rate Limiting**: Adjust delays based on target server capacity
- **Search Engines**: Customize which search engines to use
- **Export Formats**: Choose appropriate format for your use case

## File Structure

```
email_finder/
├── README.md                      # This file
├── installer.sh                   # Core dependency installer
├── run_enumeration.sh             # Main runner script
├── scripts/                       # Python, runner, and setup scripts
│   ├── email_checker.py
│   ├── whois_email_checker.py
│   ├── search_email_checker.py
│   ├── gpg_email_checker.py
│   ├── emailharvester_checker.py
│   ├── theharvester_checker.py
│   ├── web_email_finder.py
│   ├── run_email_checker.sh
│   ├── run_whois_email_checker.sh
│   ├── run_search_email_checker.sh
│   ├── run_gpg_email_checker.sh
│   ├── run_emailharvester_checker.sh
│   ├── run_theharvester_checker.sh
│   ├── setup_whois.sh
│   ├── setup_search.sh
│   ├── setup_gpg.sh
│   ├── setup_emailharvester.sh
│   └── setup_theharvester.sh
├── data/                          # Requirements and test data
├── reports/                       # Documentation and reports
└── logs/                          # Runtime logs (if enabled)
```

## License

This tool suite is provided as-is for educational and security assessment purposes.
Use responsibly and in accordance with applicable laws and regulations.

## Copyright

Copyright (c) 2025-2035 Andrea Bodei - info@andreabodei.com

## Shared Virtual Environment Standard
All scripts in this project are standardized to use one shared Python virtual environment:
`/home/spabam/.venv`

You can optionally override this path with:
`RALPHCODE_VENV_DIR=/home/spabam/.venv`
