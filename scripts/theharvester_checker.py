#!/usr/bin/env python3
"""
TheHarvester Email Checker
==========================

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
Version: 2.0.1.202510210253

This script uses TheHarvester to find email addresses associated with a domain.
It leverages TheHarvester's email discovery capabilities for comprehensive email enumeration.

WHAT THIS SCRIPT DOES:
=====================
1. Uses TheHarvester to search for email addresses associated with a domain
2. Extracts and validates email addresses from TheHarvester output
3. Removes duplicates and provides comprehensive results
4. Supports multiple output formats (TXT, CSV, JSON)
5. Provides detailed statistics and reporting

USAGE:
======
python3 theharvester_checker.py <domain> [options]

REQUIREMENTS:
=============
- Python 3.6+
- TheHarvester tool installed
- Internet connection for email discovery

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
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Set, List, Dict, Optional

class TheHarvesterChecker:
    """
    TheHarvester Email Checker for finding email addresses using TheHarvester
    """
    
    def __init__(self, domain: str, output_file: Optional[str] = None, 
                 verbose: bool = False, timeout: int = 60):
        """
        Initialize the TheHarvester checker
        
        Args:
            domain: Target domain to search for
            output_file: Optional output file path
            verbose: Enable verbose logging
            timeout: Command timeout in seconds
        """
        self.domain = domain
        self.output_file = output_file
        self.verbose = verbose
        self.timeout = timeout
        
        # Results storage
        self.emails = set()
        self.stats = {
            'start_time': None,
            'end_time': None,
            'emails_found': 0,
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
║                        TheHarvester Email Checker                          ║
║                                                                              ║
║  Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com                ║
║  Version: 2.0.1.202510210253                                                  ║
║                                                                              ║
║  This tool uses TheHarvester to find email addresses associated with         ║
║  a domain. It leverages TheHarvester's email discovery capabilities.         ║
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
    
    def check_theharvester_installed(self) -> bool:
        """
        Check if TheHarvester is installed and accessible
        
        Returns:
            True if installed, False otherwise
        """
        try:
            # Try to run theharvester --help
            result = subprocess.run(
                ['theharvester', '--help'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            # Try alternative command
            try:
                result = subprocess.run(
                    ['python3', '-m', 'theHarvester', '--help'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                return result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                return False
    
    def run_theharvester(self) -> Set[str]:
        """
        Run TheHarvester to find email addresses
        
        Returns:
            Set of found email addresses
        """
        emails = set()
        
        try:
            if self.verbose:
                print(f"🔍 Running TheHarvester for {self.domain}...")
            
            # Check if TheHarvester is installed
            if not self.check_theharvester_installed():
                if self.verbose:
                    print("  ❌ TheHarvester is not installed or not in PATH")
                self.stats['errors'] += 1
                return emails
            
            # Try different TheHarvester command variations
            commands = [
                ['theharvester', '-d', self.domain, '-b', 'all'],
                ['theharvester', '-d', self.domain, '-b', 'google,bing,yahoo'],
                ['python3', '-m', 'theHarvester', '-d', self.domain, '-b', 'all'],
                ['python3', '-m', 'theHarvester', '-d', self.domain, '-b', 'google,bing,yahoo']
            ]
            
            for cmd in commands:
                try:
                    if self.verbose:
                        print(f"  📝 Trying command: {' '.join(cmd)}")
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=self.timeout
                    )
                    
                    if result.returncode == 0:
                        # Parse output for email addresses
                        output = result.stdout
                        if self.verbose:
                            print(f"  📄 Output length: {len(output)} characters")
                        
                        # Extract emails from output
                        found_emails = self.email_regex.findall(output)
                        
                        for email in found_emails:
                            if self.is_valid_email(email):
                                emails.add(email.lower())
                                if self.verbose:
                                    print(f"  ✅ Found: {email}")
                        
                        if self.verbose:
                            print(f"  📊 Total valid emails found: {len(emails)}")
                        
                        # If we found emails, we can stop trying other commands
                        if emails:
                            break
                    else:
                        if self.verbose:
                            print(f"  ❌ Command failed with return code: {result.returncode}")
                            if result.stderr:
                                print(f"  📄 Error output: {result.stderr}")
                
                except subprocess.TimeoutExpired:
                    if self.verbose:
                        print(f"  ⏰ Command timed out after {self.timeout} seconds")
                    continue
                except Exception as e:
                    if self.verbose:
                        print(f"  ❌ Error running command: {e}")
                    continue
            
            if not emails:
                self.stats['errors'] += 1
            
        except Exception as e:
            if self.verbose:
                print(f"  ❌ Error running TheHarvester: {e}")
            self.stats['errors'] += 1
        
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
            f.write(f"# TheHarvester Email Checker Results for {self.domain}\n")
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
                writer.writerow([email, self.domain, 'TheHarvester'])
    
    def print_summary(self, emails: Set[str]):
        """Print summary of results"""
        print(f"\n{'='*60}")
        print(f"📊 THEHARVESTER EMAIL SEARCH SUMMARY")
        print(f"{'='*60}")
        print(f"Target Domain: {self.domain}")
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
            print(f"\n❌ No emails found using TheHarvester")
        
        print(f"\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")
    
    def run_search(self) -> bool:
        """
        Run the complete TheHarvester email search process
        
        Returns:
            True if successful, False otherwise
        """
        self.print_banner()
        
        print(f"🎯 Starting TheHarvester search for: {self.domain}")
        
        self.stats['start_time'] = datetime.now()
        
        # Run TheHarvester
        self.emails = self.run_theharvester()
        
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
        description='TheHarvester Email Checker - Find emails using TheHarvester\n\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic TheHarvester email search
  python3 theharvester_checker.py example.com
  
  # With output file
  python3 theharvester_checker.py example.com --output emails.txt
  
  # JSON output
  python3 theharvester_checker.py example.com --output emails.json
  
  # CSV output
  python3 theharvester_checker.py example.com --output emails.csv
  
  # Verbose output
  python3 theharvester_checker.py example.com --verbose
  
  # Show banner
  python3 theharvester_checker.py --banner

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
        """
    )
    
    parser.add_argument('domain', nargs='?', help='Target domain to search for')
    parser.add_argument('--output', '-o', help='Output file path (supports .txt, .json, .csv)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--timeout', '-t', type=int, default=60, help='Command timeout in seconds (default: 60)')
    parser.add_argument('--banner', action='store_true', help='Show banner and exit')
    
    args = parser.parse_args()
    
    # Handle banner display
    if args.banner:
        checker = TheHarvesterChecker('example.com')
        checker.print_banner()
        sys.exit(0)
    
    # Validate arguments
    if not args.domain:
        print("Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")
        parser.error("Domain is required")
    
    # Create checker instance
    checker = TheHarvesterChecker(
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

