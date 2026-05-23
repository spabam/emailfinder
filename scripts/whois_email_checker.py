#!/usr/bin/env python3
"""
Whois Email Checker and Extractor
=================================

Copyright (c) 2015-2035 Andrea Bodei
Email: info@andreabodei.com
Version: 2.0.1.202510210253

This tool is designed to extract email addresses from whois output for domains.
It provides comprehensive email discovery capabilities for legitimate purposes such as
contact information gathering, security assessments, and compliance checking.

WHAT THIS TOOL DOES:
===================
1. Executes whois queries for specified domains
2. Resolves domain names to IP addresses and performs whois on IPs
3. Extracts email addresses from whois output using advanced regex patterns
4. Validates and deduplicates email addresses
5. Outputs results in organized, sorted lists
6. Provides comprehensive reporting and statistics
7. Supports multiple output formats (text, CSV, JSON)

SECURITY USE CASES:
==================
- Security assessments and penetration testing
- Contact information gathering for legitimate purposes
- Compliance checking and data discovery
- Domain ownership verification and contact discovery
- Email address inventory and management

FEATURES:
=========
- Advanced email pattern matching from whois output
- Domain to IP resolution and IP whois queries
- Duplicate detection and removal
- Domain validation and error handling
- Comprehensive reporting and statistics
- Export capabilities (text, CSV, JSON)
- Batch processing for multiple domains

USAGE EXAMPLES:
==============
Basic usage:
    python3 whois_email_checker.py example.com

Multiple domains:
    python3 whois_email_checker.py example.com google.com github.com

With output file:
    python3 whois_email_checker.py example.com --output emails.txt

With CSV export:
    python3 whois_email_checker.py example.com --output emails.csv --format csv

SECURITY CONSIDERATIONS:
=======================
- This tool is designed for legitimate security assessments and research
- Only queries publicly available whois information
- Use responsibly and in accordance with applicable laws and regulations
- Always obtain proper authorization before testing

REQUIREMENTS:
============
- Python 3.6+
- whois command-line tool
- Internet connection

LICENSE:
========
This tool is provided as-is for educational and security assessment purposes.
Use responsibly and in accordance with applicable laws and regulations.
"""

import subprocess
import re
import argparse
import sys
import logging
import json
import csv
import socket
from typing import Set, List, Dict, Optional
from collections import defaultdict, Counter
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WhoisEmailChecker:
    """
    Whois Email Checker and Extractor Class
    
    This class provides functionality to:
    - Execute whois queries for domains
    - Resolve domains to IP addresses and query IP whois
    - Extract email addresses from whois output
    - Validate and deduplicate email addresses
    - Generate comprehensive reports
    """
    
    def __init__(self):
        """
        Initialize the Whois Email Checker
        """
        # Email patterns for extraction from whois output
        self.email_patterns = [
            # Standard email pattern
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            # Email with obfuscation patterns
            r'\b[A-Za-z0-9._%+-]+\s*\[at\]\s*[A-Za-z0-9.-]+\s*\[dot\]\s*[A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.\s*[A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%+-]+\s*\(at\)\s*[A-Za-z0-9.-]+\s*\(dot\)\s*[A-Z|a-z]{2,}\b',
            # Email in specific whois fields
            r'Registrant\s+Email:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'Admin\s+Email:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'Tech\s+Email:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'Billing\s+Email:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'Email:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'Contact\s+Email:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        ]
        
        # Compile regex patterns
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.email_patterns]
        
        # Statistics
        self.stats = {
            'domains_queried': 0,
            'ips_queried': 0,
            'emails_found': 0,
            'unique_emails': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Results storage
        self.domain_emails = defaultdict(set)  # domain -> set of emails
        self.ip_emails = defaultdict(set)      # ip -> set of emails
        self.all_emails = set()
    
    def is_valid_email(self, email: str) -> bool:
        """
        Validate email address format
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email is valid, False otherwise
        """
        # Clean email
        email = email.strip().lower()
        
        # Basic validation
        if not email or len(email) > 254:
            return False
        
        # Check for common invalid patterns
        invalid_patterns = [
            r'^[^@]+$',  # No @ symbol
            r'^@.*',     # Starts with @
            r'.*@$',     # Ends with @
            r'\.{2,}',   # Multiple consecutive dots
            r'^\.',      # Starts with dot
            r'\.$',      # Ends with dot
            r'@.*@',     # Multiple @ symbols
            r'[<>]',     # Contains angle brackets
            r'^\s|\s$',  # Leading or trailing whitespace
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, email):
                return False
        
        # Check for valid domain
        parts = email.split('@')
        if len(parts) != 2:
            return False
        
        local, domain = parts
        
        # Validate local part
        if not local or len(local) > 64:
            return False
        
        # Validate domain
        if not domain or len(domain) > 253:
            return False
        
        # Check domain has at least one dot
        if '.' not in domain:
            return False
        
        # Check for valid TLD
        tld = domain.split('.')[-1]
        if len(tld) < 2 or not tld.isalpha():
            return False
        
        return True
    
    def clean_email(self, email: str) -> str:
        """
        Clean and normalize email address
        
        Args:
            email: Raw email address
            
        Returns:
            Cleaned email address
        """
        # Remove common obfuscation
        email = email.replace('[at]', '@').replace('[dot]', '.')
        email = email.replace('(at)', '@').replace('(dot)', '.')
        email = email.replace(' at ', '@').replace(' dot ', '.')
        
        # Remove quotes and brackets
        email = re.sub(r'["\'<>]', '', email)
        
        # Remove extra whitespace
        email = email.strip()
        
        return email.lower()
    
    def extract_emails_from_text(self, text: str) -> Set[str]:
        """
        Extract email addresses from whois text using multiple patterns
        
        Args:
            text: Whois text content to search
            
        Returns:
            Set of found email addresses
        """
        emails = set()
        
        for pattern in self.compiled_patterns:
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]  # Extract from group
                
                cleaned = self.clean_email(match)
                if self.is_valid_email(cleaned):
                    emails.add(cleaned)
        
        return emails
    
    def resolve_domain_to_ip(self, domain: str) -> Optional[str]:
        """
        Resolve domain name to IP address
        
        Args:
            domain: Domain name to resolve
            
        Returns:
            IP address string or None if failed
        """
        try:
            logger.info(f"Resolving domain to IP: {domain}")
            
            # Remove protocol if present
            if domain.startswith(('http://', 'https://')):
                domain = domain.split('://')[1]
            
            # Remove port if present
            if ':' in domain:
                domain = domain.split(':')[0]
            
            # Resolve domain to IP
            ip_address = socket.gethostbyname(domain)
            logger.info(f"Resolved {domain} to {ip_address}")
            return ip_address
            
        except socket.gaierror as e:
            logger.warning(f"Failed to resolve {domain} to IP: {e}")
            return None
        except Exception as e:
            logger.error(f"Error resolving {domain} to IP: {e}")
            return None
    
    def execute_whois(self, target: str) -> Optional[str]:
        """
        Execute whois query for a domain or IP address
        
        Args:
            target: Domain or IP address to query
            
        Returns:
            Whois output text or None if failed
        """
        try:
            logger.info(f"Querying whois for: {target}")
            
            # Execute whois command
            result = subprocess.run(
                ['whois', target],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                logger.error(f"Whois query failed for {target}: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"Whois query timeout for {target}")
            return None
        except FileNotFoundError:
            logger.error("Whois command not found. Please install whois package.")
            return None
        except Exception as e:
            logger.error(f"Error executing whois for {target}: {e}")
            return None
    
    def check_domain(self, domain: str) -> Dict:
        """
        Check a single domain for email addresses (both domain and IP whois)
        
        Args:
            domain: Domain to check
            
        Returns:
            Dictionary with results
        """
        result = {
            'domain': domain,
            'ip_address': None,
            'emails': set(),
            'domain_emails': set(),
            'ip_emails': set(),
            'error': None,
            'domain_whois_available': False,
            'ip_whois_available': False
        }
        
        # Execute whois query for domain
        domain_whois_output = self.execute_whois(domain)
        
        if domain_whois_output:
            result['domain_whois_available'] = True
            # Extract emails from domain whois output
            domain_emails = self.extract_emails_from_text(domain_whois_output)
            result['domain_emails'] = domain_emails
            result['emails'].update(domain_emails)
            
            # Update statistics
            self.stats['domains_queried'] += 1
            self.domain_emails[domain] = domain_emails
            self.all_emails.update(domain_emails)
            
            logger.info(f"Found {len(domain_emails)} emails from domain whois for {domain}")
        else:
            logger.warning(f"Failed to get domain whois information for {domain}")
        
        # Resolve domain to IP and query IP whois
        ip_address = self.resolve_domain_to_ip(domain)
        if ip_address:
            result['ip_address'] = ip_address
            
            # Execute whois query for IP
            ip_whois_output = self.execute_whois(ip_address)
            
            if ip_whois_output:
                result['ip_whois_available'] = True
                # Extract emails from IP whois output
                ip_emails = self.extract_emails_from_text(ip_whois_output)
                result['ip_emails'] = ip_emails
                result['emails'].update(ip_emails)
                
                # Update statistics
                self.stats['ips_queried'] += 1
                self.ip_emails[ip_address] = ip_emails
                self.all_emails.update(ip_emails)
                
                logger.info(f"Found {len(ip_emails)} emails from IP whois for {ip_address}")
            else:
                logger.warning(f"Failed to get IP whois information for {ip_address}")
        else:
            logger.warning(f"Failed to resolve {domain} to IP address")
        
        # Update final statistics
        self.stats['emails_found'] += len(result['emails'])
        self.stats['unique_emails'] = len(self.all_emails)
        
        if not result['domain_whois_available'] and not result['ip_whois_available']:
            result['error'] = "Failed to retrieve any whois information"
            self.stats['errors'] += 1
        
        logger.info(f"Total emails found for {domain}: {len(result['emails'])} (domain: {len(result['domain_emails'])}, IP: {len(result['ip_emails'])})")
        
        return result
    
    def check_domains(self, domains: List[str]) -> Dict:
        """
        Check multiple domains for email addresses
        
        Args:
            domains: List of domains to check
            
        Returns:
            Dictionary with comprehensive results
        """
        logger.info(f"Starting whois email extraction for {len(domains)} domains")
        self.stats['start_time'] = datetime.now()
        
        results = []
        
        for domain in domains:
            result = self.check_domain(domain)
            results.append(result)
        
        self.stats['end_time'] = datetime.now()
        
        # Prepare comprehensive results
        comprehensive_results = {
            'domains': results,
            'all_emails': sorted(list(self.all_emails)),
            'domain_emails': dict(self.domain_emails),
            'ip_emails': dict(self.ip_emails),
            'stats': self.stats
        }
        
        return comprehensive_results
    
    def export_results(self, results: Dict, output_file: str, format: str = 'txt'):
        """
        Export results to file
        
        Args:
            results: Whois results
            output_file: Output file path
            format: Export format ('txt', 'csv', 'json')
        """
        try:
            if format == 'txt':
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("Whois Email Checker Results\n")
                    f.write("=" * 50 + "\n\n")
                    
                    f.write(f"Domains Queried: {results['stats']['domains_queried']}\n")
                    f.write(f"IPs Queried: {results['stats']['ips_queried']}\n")
                    f.write(f"Emails Found: {results['stats']['emails_found']}\n")
                    f.write(f"Unique Emails: {results['stats']['unique_emails']}\n")
                    f.write(f"Errors: {results['stats']['errors']}\n\n")
                    
                    if results['stats']['start_time'] and results['stats']['end_time']:
                        duration = results['stats']['end_time'] - results['stats']['start_time']
                        f.write(f"Duration: {duration}\n\n")
                    
                    f.write("All Email Addresses Found:\n")
                    f.write("-" * 30 + "\n")
                    for email in results['all_emails']:
                        f.write(f"{email}\n")
                    
                    f.write(f"\nEmails by Domain:\n")
                    f.write("-" * 30 + "\n")
                    for domain, emails in results['domain_emails'].items():
                        if emails:
                            f.write(f"\n{domain}:\n")
                            for email in sorted(emails):
                                f.write(f"  {email}\n")
                    
                    f.write(f"\nEmails by IP Address:\n")
                    f.write("-" * 30 + "\n")
                    for ip, emails in results['ip_emails'].items():
                        if emails:
                            f.write(f"\n{ip}:\n")
                            for email in sorted(emails):
                                f.write(f"  {email}\n")
            
            elif format == 'csv':
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Email', 'Source', 'Source_Type', 'Email_Domain'])
                    
                    # Add domain emails
                    for domain, emails in results['domain_emails'].items():
                        for email in emails:
                            email_domain = email.split('@')[1] if '@' in email else ''
                            writer.writerow([email, domain, 'Domain', email_domain])
                    
                    # Add IP emails
                    for ip, emails in results['ip_emails'].items():
                        for email in emails:
                            email_domain = email.split('@')[1] if '@' in email else ''
                            writer.writerow([email, ip, 'IP', email_domain])
            
            elif format == 'json':
                # Convert sets to lists for JSON serialization
                json_results = results.copy()
                json_results['all_emails'] = list(json_results['all_emails'])
                json_results['domain_emails'] = {k: list(v) for k, v in json_results['domain_emails'].items()}
                json_results['ip_emails'] = {k: list(v) for k, v in json_results['ip_emails'].items()}
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(json_results, f, indent=2, default=str)
            
            logger.info(f"Results exported to {output_file}")
            
        except Exception as e:
            logger.error(f"Error exporting results: {e}")

def print_banner():
    """
    Print the tool banner and manifest with usage instructions.
    """
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        Whois Email Checker and Extractor                    ║
║                                                                              ║
║  Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com                     ║
║  Version: 2.0.1.202510210253                                                  ║
║                                                                              ║
║  This tool extracts email addresses from whois output:                      ║
║  • Advanced email pattern matching from whois data                          ║
║  • Domain to IP resolution and IP whois queries                             ║
║  • Duplicate detection and removal                                          ║
║  • Domain validation and error handling                                     ║
║  • Comprehensive reporting and export capabilities                          ║
║                                                                              ║
║  USAGE EXAMPLES:                                                             ║
║  ──────────────────────────────────────────────────────────────────────────  ║
║  Basic:        python3 whois_email_checker.py example.com                   ║
║  Multiple:     python3 whois_email_checker.py example.com google.com        ║
║  With output:  python3 whois_email_checker.py example.com --output emails.txt ║
║  CSV export:   python3 whois_email_checker.py example.com --output emails.csv --format csv ║
║                                                                              ║
║  SECURITY NOTE: Use responsibly and in accordance with applicable laws      ║
║  and regulations. Always obtain proper authorization before testing.        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """
    Main function that handles command line arguments and orchestrates the whois email extraction process.
    """
    parser = argparse.ArgumentParser(
        description='Whois Email Checker and Extractor - Email Discovery from Whois Data\n\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic whois email extraction
  python whois_email_checker.py example.com
  
  # Multiple domains
  python whois_email_checker.py example.com google.com github.com
  
  # With output file
  python whois_email_checker.py example.com --output emails.txt
  
  # Export in different formats
  python whois_email_checker.py example.com --output results.json --format json
  python whois_email_checker.py example.com --output results.csv --format csv

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
        """
    )
    
    parser.add_argument('domains', nargs='*', help='Domain(s) to query for email addresses')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', choices=['txt', 'csv', 'json'], default='txt',
                       help='Output format (default: txt)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--banner', action='store_true',
                       help='Show tool banner and exit')
    
    args = parser.parse_args()
    
    # Handle banner display
    if args.banner:
        print_banner()
        sys.exit(0)
    
    # Validate arguments
    if not args.domains and not args.banner:
        print("Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")
        parser.error("At least one domain is required unless using --banner option")
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create checker instance
    checker = WhoisEmailChecker()
    
    # Start checking
    print(f"🔍 Starting whois email extraction for {len(args.domains)} domain(s)")
    print(f"📋 Domains: {', '.join(args.domains)}")
    print("=" * 60)
    
    try:
        results = checker.check_domains(args.domains)
        
        # Display results
        print(f"\n📊 WHOIS RESULTS:")
        print(f"   Domains queried: {results['stats']['domains_queried']}")
        print(f"   IPs queried: {results['stats']['ips_queried']}")
        print(f"   Emails found: {results['stats']['emails_found']}")
        print(f"   Unique emails: {results['stats']['unique_emails']}")
        print(f"   Errors: {results['stats']['errors']}")
        
        if results['stats']['start_time'] and results['stats']['end_time']:
            duration = results['stats']['end_time'] - results['stats']['start_time']
            print(f"   Duration: {duration}")
        
        print("=" * 60)
        
        if results['all_emails']:
            print(f"\n📧 EMAIL ADDRESSES FOUND ({len(results['all_emails'])}):")
            print("-" * 40)
            for i, email in enumerate(results['all_emails'], 1):
                print(f"{i:3d}. {email}")
        else:
            print("\n❌ No email addresses found")
        
        # Export results if requested
        if args.output:
            checker.export_results(results, args.output, args.format)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Email extraction interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during email extraction: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
