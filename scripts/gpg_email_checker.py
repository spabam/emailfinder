#!/usr/bin/env python3
"""
GPG/PGP Email Checker
====================

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
Version: 2.0.1.202510210253

This script searches GPG/PGP key servers for email addresses associated with a domain.
It queries multiple GPG key servers to find registered email addresses.

WHAT THIS SCRIPT DOES:
=====================
1. Searches GPG key servers for email addresses associated with a domain
2. Queries multiple key servers (keys.openpgp.org, pgp.mit.edu, keyserver.ubuntu.com)
3. Extracts and validates email addresses from GPG key data
4. Removes duplicates and provides comprehensive results
5. Supports multiple output formats (TXT, CSV, JSON)

USAGE:
======
python3 gpg_email_checker.py <domain> [options]

REQUIREMENTS:
=============
- Python 3.6+
- requests library
- Internet connection for GPG key server access

LICENSE:
========
This script is provided as-is for educational and security assessment purposes.
Use responsibly and in accordance with applicable laws and regulations.
"""

import sys
import os
import re
import json
import csv
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Set, List, Dict, Optional
import requests
from urllib.parse import quote

class GPGEmailChecker:
    """
    GPG/PGP Email Checker for finding email addresses in GPG key servers
    """
    
    def __init__(self, domain: str, output_file: Optional[str] = None, 
                 verbose: bool = False, timeout: int = 10):
        """
        Initialize the GPG email checker
        
        Args:
            domain: Target domain to search for
            output_file: Optional output file path
            verbose: Enable verbose logging
            timeout: Request timeout in seconds
        """
        self.domain = domain
        self.output_file = output_file
        self.verbose = verbose
        self.timeout = timeout
        
        # GPG key servers to query
        self.key_servers = [
            'https://keys.openpgp.org/vks/v1/by-fingerprint/',
            'https://pgp.mit.edu/pks/lookup',
            'https://keyserver.ubuntu.com/pks/lookup'
        ]
        
        # Results storage
        self.emails = set()
        self.stats = {
            'start_time': None,
            'end_time': None,
            'emails_found': 0,
            'servers_queried': 0,
            'errors': 0
        }
        
        # Email validation regex
        self.email_regex = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
    
    def print_banner(self):
        """Print the tool banner"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        GPG/PGP Email Checker                               ║
║                                                                              ║
║  Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com                ║
║  Version: 2.0.1.202510210253                                                  ║
║                                                                              ║
║  This tool searches GPG/PGP key servers for email addresses associated      ║
║  with a domain. It queries multiple key servers to find registered emails.  ║
║                                                                              ║
║  SECURITY NOTE: Use responsibly and in accordance with applicable laws      ║
║  and regulations. Always obtain proper authorization before testing.        ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
    
    def is_valid_email(self, email: str) -> bool:
        """
        Validate email address format and domain
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email or '@' not in email:
            return False
        
        # Check if email ends with target domain
        if not email.lower().endswith(f'@{self.domain.lower()}'):
            return False
        
        # Basic email format validation
        if not self.email_regex.match(email):
            return False
        
        return True
    
    def search_keyserver_openpgp(self) -> Set[str]:
        """
        Search keys.openpgp.org for GPG keys
        
        Returns:
            Set of found email addresses
        """
        emails = set()
        
        try:
            if self.verbose:
                print(f"🔍 Searching keys.openpgp.org for {self.domain}...")
            
            # Search by domain using the search endpoint
            search_url = f"https://keys.openpgp.org/vks/v1/by-email/{self.domain}"
            
            # Try different search approaches
            search_urls = [
                f"https://keys.openpgp.org/vks/v1/by-email/{self.domain}",
                f"https://keys.openpgp.org/vks/v1/search?q={self.domain}",
                f"https://keys.openpgp.org/vks/v1/by-fingerprint/{self.domain}"
            ]
            
            for url in search_urls:
                try:
                    response = requests.get(url, timeout=self.timeout)
                    if response.status_code == 200:
                        # Extract emails from response
                        content = response.text
                        found_emails = self.email_regex.findall(content)
                        
                        for email in found_emails:
                            if self.is_valid_email(email):
                                emails.add(email.lower())
                                if self.verbose:
                                    print(f"  ✅ Found: {email}")
                        break
                    elif response.status_code == 404:
                        # No results found, continue to next URL
                        continue
                    else:
                        response.raise_for_status()
                except requests.exceptions.RequestException:
                    continue
            
            self.stats['servers_queried'] += 1
            
        except Exception as e:
            self.stats['errors'] += 1
            if self.verbose:
                print(f"  ❌ Error searching keys.openpgp.org: {e}")
        
        return emails
    
    def search_keyserver_mit(self) -> Set[str]:
        """
        Search pgp.mit.edu for GPG keys
        
        Returns:
            Set of found email addresses
        """
        emails = set()
        
        try:
            if self.verbose:
                print(f"🔍 Searching pgp.mit.edu for {self.domain}...")
            
            # Search by domain with different parameters
            search_urls = [
                f"https://pgp.mit.edu/pks/lookup?search={quote(self.domain)}&op=index",
                f"https://pgp.mit.edu/pks/lookup?search={quote(self.domain)}&op=vindex",
                f"https://pgp.mit.edu/pks/lookup?search={quote(self.domain)}&op=get"
            ]
            
            for url in search_urls:
                try:
                    response = requests.get(url, timeout=self.timeout)
                    if response.status_code == 200:
                        # Extract emails from response
                        content = response.text
                        found_emails = self.email_regex.findall(content)
                        
                        for email in found_emails:
                            if self.is_valid_email(email):
                                emails.add(email.lower())
                                if self.verbose:
                                    print(f"  ✅ Found: {email}")
                        break
                    elif response.status_code == 404:
                        # No results found, continue to next URL
                        continue
                    else:
                        response.raise_for_status()
                except requests.exceptions.RequestException:
                    continue
            
            self.stats['servers_queried'] += 1
            
        except Exception as e:
            self.stats['errors'] += 1
            if self.verbose:
                print(f"  ❌ Error searching pgp.mit.edu: {e}")
        
        return emails
    
    def search_keyserver_ubuntu(self) -> Set[str]:
        """
        Search keyserver.ubuntu.com for GPG keys
        
        Returns:
            Set of found email addresses
        """
        emails = set()
        
        try:
            if self.verbose:
                print(f"🔍 Searching keyserver.ubuntu.com for {self.domain}...")
            
            # Search by domain with different parameters
            search_urls = [
                f"https://keyserver.ubuntu.com/pks/lookup?search={quote(self.domain)}&op=index",
                f"https://keyserver.ubuntu.com/pks/lookup?search={quote(self.domain)}&op=vindex",
                f"https://keyserver.ubuntu.com/pks/lookup?search={quote(self.domain)}&op=get"
            ]
            
            for url in search_urls:
                try:
                    response = requests.get(url, timeout=self.timeout)
                    if response.status_code == 200:
                        # Extract emails from response
                        content = response.text
                        found_emails = self.email_regex.findall(content)
                        
                        for email in found_emails:
                            if self.is_valid_email(email):
                                emails.add(email.lower())
                                if self.verbose:
                                    print(f"  ✅ Found: {email}")
                        break
                    elif response.status_code == 404:
                        # No results found, continue to next URL
                        continue
                    else:
                        response.raise_for_status()
                except requests.exceptions.RequestException:
                    continue
            
            self.stats['servers_queried'] += 1
            
        except Exception as e:
            self.stats['errors'] += 1
            if self.verbose:
                print(f"  ❌ Error searching keyserver.ubuntu.com: {e}")
        
        return emails
    
    def search_gpg_keys(self) -> Set[str]:
        """
        Search all GPG key servers for email addresses
        
        Returns:
            Set of unique email addresses found
        """
        all_emails = set()
        
        print(f"🎯 Starting GPG key search for: {self.domain}")
        
        # Search each key server
        all_emails.update(self.search_keyserver_openpgp())
        time.sleep(1)  # Rate limiting
        
        all_emails.update(self.search_keyserver_mit())
        time.sleep(1)  # Rate limiting
        
        all_emails.update(self.search_keyserver_ubuntu())
        
        # If no results found, try searching for common email patterns
        if not all_emails:
            if self.verbose:
                print(f"🔍 No results found, trying common email patterns...")
            all_emails.update(self.search_common_patterns())
        
        return all_emails
    
    def search_common_patterns(self) -> Set[str]:
        """
        Search for common email patterns associated with the domain
        
        Returns:
            Set of found email addresses
        """
        emails = set()
        
        # Common email patterns to search for
        common_patterns = [
            f"admin@{self.domain}",
            f"contact@{self.domain}",
            f"info@{self.domain}",
            f"support@{self.domain}",
            f"webmaster@{self.domain}",
            f"postmaster@{self.domain}",
            f"root@{self.domain}",
            f"noreply@{self.domain}",
            f"no-reply@{self.domain}"
        ]
        
        for pattern in common_patterns:
            try:
                if self.verbose:
                    print(f"  🔍 Searching for: {pattern}")
                
                # Search each keyserver for this specific email
                for server in ['openpgp', 'mit', 'ubuntu']:
                    try:
                        if server == 'openpgp':
                            url = f"https://keys.openpgp.org/vks/v1/by-email/{pattern}"
                        elif server == 'mit':
                            url = f"https://pgp.mit.edu/pks/lookup?search={quote(pattern)}&op=index"
                        else:  # ubuntu
                            url = f"https://keyserver.ubuntu.com/pks/lookup?search={quote(pattern)}&op=index"
                        
                        response = requests.get(url, timeout=self.timeout)
                        if response.status_code == 200:
                            content = response.text
                            found_emails = self.email_regex.findall(content)
                            
                            for email in found_emails:
                                if self.is_valid_email(email):
                                    emails.add(email.lower())
                                    if self.verbose:
                                        print(f"    ✅ Found: {email}")
                            break  # Found results, no need to check other servers
                        
                    except requests.exceptions.RequestException:
                        continue
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                if self.verbose:
                    print(f"    ❌ Error searching for {pattern}: {e}")
                continue
        
        return emails
    
    def save_results(self, emails: Set[str]):
        """Save results to file if specified"""
        if not self.output_file:
            return
        
        output_path = Path(self.output_file)
        file_extension = output_path.suffix.lower()
        
        try:
            if file_extension == '.json':
                self.save_json(emails)
            elif file_extension == '.csv':
                self.save_csv(emails)
            else:
                self.save_txt(emails)
            
            print(f"📁 Results saved to: {self.output_file}")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def save_txt(self, emails: Set[str]):
        """Save results as text file"""
        with open(self.output_file, 'w') as f:
            f.write(f"# GPG/PGP Email Checker Results for {self.domain}\n")
            f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com\n")
            f.write(f"# Total emails found: {len(emails)}\n\n")
            
            for email in sorted(emails):
                f.write(f"{email}\n")
    
    def save_json(self, emails: Set[str]):
        """Save results as JSON file"""
        data = {
            'domain': self.domain,
            'timestamp': datetime.now().isoformat(),
            'copyright': 'Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com',
            'statistics': {
                'start_time': self.stats['start_time'].isoformat() if self.stats['start_time'] else None,
                'end_time': self.stats['end_time'].isoformat() if self.stats['end_time'] else None,
                'emails_found': len(emails),
                'servers_queried': self.stats['servers_queried'],
                'errors': self.stats['errors']
            },
            'emails': sorted(list(emails))
        }
        
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_csv(self, emails: Set[str]):
        """Save results as CSV file"""
        with open(self.output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['# Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com'])
            writer.writerow(['Email', 'Domain', 'Source'])
            
            for email in sorted(emails):
                writer.writerow([email, self.domain, 'GPG'])
    
    def print_summary(self, emails: Set[str]):
        """Print summary of results"""
        print(f"\n{'='*60}")
        print(f"📊 GPG/PGP EMAIL SEARCH SUMMARY")
        print(f"{'='*60}")
        print(f"Target Domain: {self.domain}")
        print(f"Servers Queried: {self.stats['servers_queried']}")
        print(f"Emails Found: {len(emails)}")
        print(f"Errors: {self.stats['errors']}")
        
        if self.stats['start_time'] and self.stats['end_time']:
            duration = self.stats['end_time'] - self.stats['start_time']
            print(f"Duration: {duration}")
        
        if emails:
            print(f"\n📧 EMAIL ADDRESSES FOUND ({len(emails)}):")
            print("-" * 40)
            for i, email in enumerate(sorted(emails), 1):
                print(f"{i:3d}. {email}")
        else:
            print(f"\n❌ No emails found in GPG key servers")
        
        print(f"\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")
    
    def run_search(self) -> bool:
        """
        Run the complete GPG email search process
        
        Returns:
            True if successful, False otherwise
        """
        self.print_banner()
        
        print(f"🎯 Starting GPG key search for: {self.domain}")
        
        self.stats['start_time'] = datetime.now()
        
        # Search GPG key servers
        self.emails = self.search_gpg_keys()
        
        self.stats['end_time'] = datetime.now()
        self.stats['emails_found'] = len(self.emails)
        
        # Save results if output file specified
        if self.output_file:
            self.save_results(self.emails)
        
        # Print summary
        self.print_summary(self.emails)
        
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='GPG/PGP Email Checker - Find emails in GPG key servers\n\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic GPG email search
  python3 gpg_email_checker.py example.com
  
  # With output file
  python3 gpg_email_checker.py example.com --output emails.txt
  
  # JSON output
  python3 gpg_email_checker.py example.com --output emails.json
  
  # CSV output
  python3 gpg_email_checker.py example.com --output emails.csv
  
  # Verbose output
  python3 gpg_email_checker.py example.com --verbose
  
  # Show banner
  python3 gpg_email_checker.py --banner

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
        """
    )
    
    parser.add_argument('domain', nargs='?', help='Target domain to search for')
    parser.add_argument('--output', '-o', help='Output file path (supports .txt, .json, .csv)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--timeout', '-t', type=int, default=10, help='Request timeout in seconds (default: 10)')
    parser.add_argument('--banner', action='store_true', help='Show banner and exit')
    
    args = parser.parse_args()
    
    # Handle banner display
    if args.banner:
        checker = GPGEmailChecker('example.com')
        checker.print_banner()
        sys.exit(0)
    
    # Validate arguments
    if not args.domain:
        print("Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")
        parser.error("Domain is required")
    
    # Create checker instance
    checker = GPGEmailChecker(
        domain=args.domain,
        output_file=args.output,
        verbose=args.verbose,
        timeout=args.timeout
    )
    
    # Run search
    try:
        success = checker.run_search()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Search interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
