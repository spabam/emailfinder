#!/usr/bin/env python3
"""
Web Email Finder
================

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
Version: 2.0.1.202510210253

This script finds email addresses by scraping websites and searching for email patterns.
It's a reliable alternative to tools that have installation or runtime issues.

WHAT THIS SCRIPT DOES:
=====================
1. Scrapes websites for email addresses using multiple methods
2. Searches common email patterns on websites
3. Extracts and validates email addresses
4. Removes duplicates and provides comprehensive results
5. Supports multiple output formats (TXT, CSV, JSON)

USAGE:
======
python3 web_email_finder.py <domain> [options]

REQUIREMENTS:
=============
- Python 3.6+
- requests library
- Internet connection

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
import requests
from datetime import datetime
from pathlib import Path
from typing import Set, List, Dict, Optional
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

class WebEmailFinder:
    """
    Web Email Finder for finding email addresses by scraping websites
    """
    
    def __init__(self, domain: str, output_file: Optional[str] = None, 
                 verbose: bool = False, timeout: int = 10, max_pages: int = 5):
        """
        Initialize the web email finder
        
        Args:
            domain: Target domain to search for
            output_file: Optional output file path
            verbose: Enable verbose logging
            timeout: Request timeout in seconds
            max_pages: Maximum number of pages to scrape
        """
        self.domain = domain
        self.output_file = output_file
        self.verbose = verbose
        self.timeout = timeout
        self.max_pages = max_pages
        
        # Results storage
        self.emails = set()
        self.stats = {
            'start_time': None,
            'end_time': None,
            'emails_found': 0,
            'pages_scraped': 0,
            'errors': 0
        }
        
        # Email validation regex
        self.email_regex = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        
        # Common email patterns to search for
        self.common_patterns = [
            f"admin@{self.domain}",
            f"contact@{self.domain}",
            f"info@{self.domain}",
            f"support@{self.domain}",
            f"webmaster@{self.domain}",
            f"postmaster@{self.domain}",
            f"root@{self.domain}",
            f"noreply@{self.domain}",
            f"no-reply@{self.domain}",
            f"sales@{self.domain}",
            f"marketing@{self.domain}",
            f"help@{self.domain}",
            f"service@{self.domain}"
        ]
        
        # Common pages to check
        self.common_pages = [
            "/",
            "/contact",
            "/contact-us",
            "/about",
            "/about-us",
            "/team",
            "/staff",
            "/support",
            "/help",
            "/privacy",
            "/terms",
            "/legal"
        ]
    
    def print_banner(self):
        """Print the tool banner"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                            Web Email Finder                                 ║
║                                                                              ║
║  Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com                ║
║  Version: 2.0.1.202510210253                                                  ║
║                                                                              ║
║  This tool finds email addresses by scraping websites and searching for      ║
║  email patterns. It's a reliable alternative to tools with installation     ║
║  or runtime issues.                                                          ║
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
    
    def can_fetch(self, url: str) -> bool:
        """
        Check if we can fetch a URL based on robots.txt
        
        Args:
            url: URL to check
            
        Returns:
            True if we can fetch, False otherwise
        """
        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            return rp.can_fetch("*", url)
        except:
            # If we can't read robots.txt, assume we can fetch
            return True
    
    def scrape_page(self, url: str) -> Set[str]:
        """
        Scrape a single page for email addresses
        
        Args:
            url: URL to scrape
            
        Returns:
            Set of found email addresses
        """
        emails = set()
        
        try:
            if self.verbose:
                print(f"  🔍 Scraping: {url}")
            
            # Check robots.txt
            if not self.can_fetch(url):
                if self.verbose:
                    print(f"    ⚠️  Blocked by robots.txt")
                return emails
            
            # Make request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, timeout=self.timeout, headers=headers)
            response.raise_for_status()
            
            # Extract emails from content
            content = response.text
            found_emails = self.email_regex.findall(content)
            
            for email in found_emails:
                if self.is_valid_email(email):
                    emails.add(email.lower())
                    if self.verbose:
                        print(f"    ✅ Found: {email}")
            
            self.stats['pages_scraped'] += 1
            
        except Exception as e:
            if self.verbose:
                print(f"    ❌ Error scraping {url}: {e}")
            self.stats['errors'] += 1
        
        return emails
    
    def search_common_patterns(self) -> Set[str]:
        """
        Search for common email patterns
        
        Returns:
            Set of found email addresses
        """
        emails = set()
        
        if self.verbose:
            print(f"🔍 Searching for common email patterns...")
        
        for pattern in self.common_patterns:
            if self.verbose:
                print(f"  🔍 Checking: {pattern}")
            
            # Try to verify if this email exists by checking common pages
            for page in self.common_pages[:3]:  # Only check first 3 pages
                try:
                    url = f"https://{self.domain}{page}"
                    if self.verbose:
                        print(f"    📄 Checking {url} for {pattern}")
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    
                    response = requests.get(url, timeout=self.timeout, headers=headers)
                    if response.status_code == 200:
                        content = response.text.lower()
                        if pattern.lower() in content:
                            emails.add(pattern.lower())
                            if self.verbose:
                                print(f"    ✅ Found pattern: {pattern}")
                            break
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    if self.verbose:
                        print(f"    ❌ Error checking {pattern}: {e}")
                    continue
        
        return emails
    
    def find_emails(self) -> Set[str]:
        """
        Find email addresses using multiple methods
        
        Returns:
            Set of found email addresses
        """
        all_emails = set()
        
        print(f"🎯 Starting web email search for: {self.domain}")
        
        # Method 1: Scrape common pages
        if self.verbose:
            print(f"🔍 Method 1: Scraping common pages...")
        
        for page in self.common_pages[:self.max_pages]:
            url = f"https://{self.domain}{page}"
            emails = self.scrape_page(url)
            all_emails.update(emails)
            
            if emails and self.verbose:
                print(f"  📊 Found {len(emails)} emails on {page}")
            
            time.sleep(1)  # Rate limiting
        
        # Method 2: Search for common email patterns
        if self.verbose:
            print(f"🔍 Method 2: Searching common email patterns...")
        
        pattern_emails = self.search_common_patterns()
        all_emails.update(pattern_emails)
        
        if pattern_emails and self.verbose:
            print(f"  📊 Found {len(pattern_emails)} emails from patterns")
        
        return all_emails
    
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
            f.write(f"# Web Email Finder Results for {self.domain}\n")
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
                'pages_scraped': self.stats['pages_scraped'],
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
                writer.writerow([email, self.domain, 'Web Scraping'])
    
    def print_summary(self, emails: Set[str]):
        """Print summary of results"""
        print(f"\n{'='*60}")
        print(f"📊 WEB EMAIL FINDER SUMMARY")
        print(f"{'='*60}")
        print(f"Target Domain: {self.domain}")
        print(f"Pages Scraped: {self.stats['pages_scraped']}")
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
            print(f"\n❌ No emails found using web scraping")
        
        print(f"\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")
    
    def run_search(self) -> bool:
        """
        Run the complete web email search process
        
        Returns:
            True if successful, False otherwise
        """
        self.print_banner()
        
        print(f"🎯 Starting web email search for: {self.domain}")
        
        self.stats['start_time'] = datetime.now()
        
        # Find emails
        self.emails = self.find_emails()
        
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
        description='Web Email Finder - Find emails by scraping websites\n\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic web email search
  python3 web_email_finder.py example.com
  
  # With output file
  python3 web_email_finder.py example.com --output emails.txt
  
  # JSON output
  python3 web_email_finder.py example.com --output emails.json
  
  # CSV output
  python3 web_email_finder.py example.com --output emails.csv
  
  # Verbose output
  python3 web_email_finder.py example.com --verbose
  
  # Show banner
  python3 web_email_finder.py --banner

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
        """
    )
    
    parser.add_argument('domain', nargs='?', help='Target domain to search for')
    parser.add_argument('--output', '-o', help='Output file path (supports .txt, .json, .csv)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--timeout', '-t', type=int, default=10, help='Request timeout in seconds (default: 10)')
    parser.add_argument('--max-pages', '-p', type=int, default=5, help='Maximum pages to scrape (default: 5)')
    parser.add_argument('--banner', action='store_true', help='Show banner and exit')
    
    args = parser.parse_args()
    
    # Handle banner display
    if args.banner:
        finder = WebEmailFinder('example.com')
        finder.print_banner()
        sys.exit(0)
    
    # Validate arguments
    if not args.domain:
        print("Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")
        parser.error("Domain is required")
    
    # Create finder instance
    finder = WebEmailFinder(
        domain=args.domain,
        output_file=args.output,
        verbose=args.verbose,
        timeout=args.timeout,
        max_pages=args.max_pages
    )
    
    # Run search
    try:
        success = finder.run_search()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Search interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

