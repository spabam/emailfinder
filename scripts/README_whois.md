# Whois Email Checker and Extractor

A comprehensive tool for extracting email addresses from whois output for domains. This tool provides powerful email discovery capabilities for legitimate security assessments, contact information gathering, and compliance checking.

## Features

- **Advanced Email Detection**: Multiple regex patterns to find various email formats in whois data
- **Intelligent Validation**: Email address validation and deduplication
- **Domain Processing**: Batch processing for multiple domains
- **Comprehensive Reporting**: Detailed statistics and progress tracking
- **Multiple Export Formats**: Text, CSV, and JSON output options
- **Error Handling**: Graceful handling of whois query failures

## Email Pattern Detection

The checker can detect emails in various formats from whois output:
- Standard email addresses: `user@domain.com`
- Obfuscated emails: `user[at]domain[dot]com`
- Whois-specific fields: `Registrant Email:`, `Admin Email:`, `Tech Email:`, etc.
- Contact information: `Contact Email:`, `Billing Email:`

## Installation

### Quick Setup

1. Run the setup script:
```bash
./setup_whois.sh
```

2. Use the run script:
```bash
./run_whois_email_checker.sh example.com
```

### Manual Setup

1. Create virtual environment:
```bash
python3 -m venv $HOME/whois_email_checker_env
```

2. Activate environment:
```bash
source $HOME/whois_email_checker_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Basic whois email extraction
python3 whois_email_checker.py example.com

# Multiple domains
python3 whois_email_checker.py example.com google.com github.com

# With output file
python3 whois_email_checker.py example.com --output emails.txt
```

### Advanced Options

```bash
# Export in different formats
python3 whois_email_checker.py example.com --output results.json --format json
python3 whois_email_checker.py example.com --output results.csv --format csv

# Verbose logging
python3 whois_email_checker.py example.com --verbose
```

### Using the Run Script

```bash
# Basic whois email extraction
./run_whois_email_checker.sh example.com

# Multiple domains
./run_whois_email_checker.sh example.com google.com github.com

# With options
./run_whois_email_checker.sh example.com --output emails.txt

# Show banner
./run_whois_email_checker.sh --banner
```

## Examples

### Basic Email Discovery

```bash
$ python3 whois_email_checker.py google.com
🔍 Starting whois email extraction for 1 domain(s)
📋 Domains: google.com
============================================================

📊 WHOIS RESULTS:
   Domains queried: 1
   Emails found: 2
   Unique emails: 2
   Errors: 0
   Duration: 0:00:00.563597
============================================================

📧 EMAIL ADDRESSES FOUND (2):
----------------------------------------
  1. abusecomplaints@markmonitor.com
  2. whoisrequest@markmonitor.com
```

### Multiple Domains

```bash
$ python3 whois_email_checker.py google.com github.com
🔍 Starting whois email extraction for 2 domain(s)
📋 Domains: google.com, github.com
============================================================

📊 WHOIS RESULTS:
   Domains queried: 2
   Emails found: 3
   Unique emails: 2
   Errors: 0
   Duration: 0:00:00.969101
============================================================

📧 EMAIL ADDRESSES FOUND (2):
----------------------------------------
  1. abusecomplaints@markmonitor.com
  2. whoisrequest@markmonitor.com
```

### Export to File

```bash
$ python3 whois_email_checker.py google.com --output whois_emails.txt
# Results saved to whois_emails.txt with detailed breakdown
```

### CSV Export

```bash
$ python3 whois_email_checker.py google.com --output results.csv --format csv
# Creates CSV with columns: Email, Domain, Email_Domain
```

## Command Line Options

- `domains`: Domain(s) to query for email addresses (required)
- `--output, -o`: Output file path
- `--format`: Output format (txt, csv, json)
- `--verbose, -v`: Enable verbose logging
- `--banner`: Show tool banner and exit

## Output Formats

### Text Format
```
Whois Email Checker Results
==================================================

Domains Queried: 2
Emails Found: 3
Unique Emails: 2
Errors: 0
Duration: 0:00:00.969101

All Email Addresses Found:
------------------------------
abusecomplaints@markmonitor.com
whoisrequest@markmonitor.com

Emails by Domain:
------------------------------

google.com:
  abusecomplaints@markmonitor.com
  whoisrequest@markmonitor.com

github.com:
  abusecomplaints@markmonitor.com
```

### CSV Format
```csv
Email,Domain,Email_Domain
abusecomplaints@markmonitor.com,google.com,markmonitor.com
whoisrequest@markmonitor.com,google.com,markmonitor.com
```

### JSON Format
```json
{
  "domains": [
    {
      "domain": "google.com",
      "emails": ["abusecomplaints@markmonitor.com", "whoisrequest@markmonitor.com"],
      "error": null,
      "whois_available": true
    }
  ],
  "all_emails": ["abusecomplaints@markmonitor.com", "whoisrequest@markmonitor.com"],
  "domain_emails": {
    "google.com": ["abusecomplaints@markmonitor.com", "whoisrequest@markmonitor.com"]
  },
  "stats": {
    "domains_queried": 1,
    "emails_found": 2,
    "unique_emails": 2,
    "errors": 0
  }
}
```

## Security Considerations

- **Legitimate Use Only**: This tool is designed for legitimate security assessments and research
- **Authorization Required**: Always obtain proper authorization before testing
- **Public Information Only**: Only queries publicly available whois information
- **Legal Compliance**: Use in accordance with applicable laws and regulations

## Use Cases

- **Security Assessments**: Email discovery for penetration testing
- **Contact Information Gathering**: Finding contact details for legitimate purposes
- **Compliance Checking**: Verifying email address exposure in domain records
- **Domain Analysis**: Analyzing contact information in domain registrations
- **Data Discovery**: Inventory of email addresses in whois records

## Requirements

- Python 3.6+
- whois command-line tool
- Internet connection

## Installation of whois Tool

### Ubuntu/Debian
```bash
sudo apt-get install whois
```

### CentOS/RHEL
```bash
sudo yum install whois
```

### macOS
```bash
brew install whois
```

## Performance Tips

- **Batch Processing**: Process multiple domains in a single command
- **Output Files**: Use output files for large-scale processing
- **Error Handling**: The tool gracefully handles whois query failures

## License

This tool is provided as-is for educational and security assessment purposes.
Use responsibly and in accordance with applicable laws and regulations.

## Copyright

Copyright (c) 2025-2035 Andrea Bodei - info@andreabodei.com

