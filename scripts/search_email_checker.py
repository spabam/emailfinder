#!/usr/bin/env python3
"""
Search Engine Email Checker and Extractor
=========================================

Copyright (c) 2015-2035 Andrea Bodei
Email: info@andreabodei.com
Version: 2.0.1.202510210253

This tool searches for email addresses related to a domain using multiple
search engines (Google, DuckDuckGo, Yahoo) and extracts email addresses
from the search results.

Features:
- Multi-search engine support (Google, DuckDuckGo, Yahoo)
- Advanced email pattern matching and validation
- Duplicate detection and removal
- Respectful searching with rate limiting
- Comprehensive reporting and export capabilities
- Professional output formatting

Usage:
    python3 search_email_checker.py <domain> [options]

Examples:
    python3 search_email_checker.py example.com
    python3 search_email_checker.py example.com --output emails.txt
    python3 search_email_checker.py example.com --output results.csv --format csv
    python3 search_email_checker.py example.com --engines google,duckduckgo
    python3 search_email_checker.py --banner

Security Note: Use responsibly and in accordance with applicable laws
and regulations. Always obtain proper authorization before testing.
"""

import argparse
import re
import sys
import time
import logging
import json
import csv
from datetime import datetime
from typing import List, Set, Dict, Optional, Tuple
from urllib.parse import quote, urljoin
import requests
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class SearchEmailChecker:
    """Search Engine Email Checker and Extractor"""
    
    def __init__(self, delay: float = 2.0, timeout: int = 10):
        """
        Initialize the Search Email Checker.
        
        Args:
            delay: Delay between requests in seconds
            timeout: Request timeout in seconds
        """
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Email regex pattern
        self.email_pattern = re.compile(
            r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
            re.IGNORECASE
        )
        
        # Search engines configuration
        self.search_engines = {
            'google': {
                'name': 'Google',
                'url': 'https://www.google.com/search',
                'params': {'q': '', 'num': 20},
                'result_selector': 'div.g',
                'link_selector': 'a[href^="/url?q="]',
                'text_selector': 'span, p, div'
            },
            'duckduckgo': {
                'name': 'DuckDuckGo',
                'url': 'https://duckduckgo.com/html',
                'params': {'q': '', 'kl': 'us-en'},
                'result_selector': 'div.result',
                'link_selector': 'a.result__a',
                'text_selector': 'span, p, div'
            },
            'yahoo': {
                'name': 'Yahoo',
                'url': 'https://search.yahoo.com/search',
                'params': {'p': '', 'n': 20},
                'result_selector': 'div.dd.algo',
                'link_selector': 'a[href]',
                'text_selector': 'span, p, div'
            }
        }
        
        # Statistics
        self.stats = {
            'domains_searched': 0,
            'emails_found': 0,
            'unique_emails': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Results storage
        self.all_emails: Set[str] = set()
        self.domain_emails: Dict[str, List[str]] = {}
        self.search_results: Dict[str, Dict] = {}

    def validate_email(self, email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email or len(email) > 254:
            return False
            
        # Basic format validation
        if not self.email_pattern.match(email):
            return False
            
        # Additional checks
        local, domain = email.rsplit('@', 1)
        if len(local) > 64 or len(domain) > 253:
            return False
            
        # Check for common invalid patterns
        invalid_patterns = [
            r'\.{2,}',  # Multiple consecutive dots
            r'^\.|\.$',  # Starts or ends with dot
            r'@.*@',     # Multiple @ symbols
            r'\.@|@\.',  # Dot adjacent to @
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, email):
                return False
                
        return True

    def clean_email(self, email: str) -> str:
        """
        Clean and normalize email address.
        
        Args:
            email: Raw email address
            
        Returns:
            Cleaned email address
        """
        # Remove common prefixes/suffixes
        email = re.sub(r'^(mailto:|email:|e-mail:)\s*', '', email, flags=re.IGNORECASE)
        email = re.sub(r'\s*$', '', email)  # Remove trailing whitespace
        
        # Convert to lowercase
        email = email.lower().strip()
        
        return email

    def extract_emails_from_text(self, text: str) -> Set[str]:
        """
        Extract email addresses from text content.
        
        Args:
            text: Text content to search
            
        Returns:
            Set of found email addresses
        """
        emails = set()
        
        if not text:
            return emails
            
        # Find all email matches
        matches = self.email_pattern.findall(text)
        
        for match in matches:
            cleaned = self.clean_email(match)
            if self.validate_email(cleaned):
                emails.add(cleaned)
                
        return emails

    def search_engine(self, domain: str, engine: str, max_results: int = 20) -> Dict:
        """
        Search for emails related to a domain using a specific search engine.
        
        Args:
            domain: Domain to search for
            engine: Search engine to use
            max_results: Maximum number of results to process
            
        Returns:
            Dictionary with search results
        """
        if engine not in self.search_engines:
            logger.error(f"Unknown search engine: {engine}")
            return {'error': f'Unknown search engine: {engine}'}
            
        engine_config = self.search_engines[engine]
        logger.info(f"Searching {engine_config['name']} for emails related to {domain}")
        
        # Construct search query
        search_query = f'"{domain}" email contact'
        
        try:
            # Prepare request parameters
            params = engine_config['params'].copy()
            if engine == 'google':
                params['q'] = search_query
            elif engine == 'duckduckgo':
                params['q'] = search_query
            elif engine == 'yahoo':
                params['p'] = search_query
                
            # Make request
            response = self.session.get(
                engine_config['url'],
                params=params,
                timeout=self.timeout,
                verify=False
            )
            response.raise_for_status()
            
            # Parse results
            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.select(engine_config['result_selector'])
            
            emails_found = set()
            processed_results = 0
            
            for result in results[:max_results]:
                if processed_results >= max_results:
                    break
                    
                # Extract text content
                text_content = result.get_text()
                result_emails = self.extract_emails_from_text(text_content)
                emails_found.update(result_emails)
                
                processed_results += 1
                
            logger.info(f"Found {len(emails_found)} emails from {engine_config['name']}")
            
            return {
                'engine': engine,
                'engine_name': engine_config['name'],
                'emails': list(emails_found),
                'results_processed': processed_results,
                'error': None
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching {engine_config['name']}: {e}")
            return {
                'engine': engine,
                'engine_name': engine_config['name'],
                'emails': [],
                'results_processed': 0,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error searching {engine_config['name']}: {e}")
            return {
                'engine': engine,
                'engine_name': engine_config['name'],
                'emails': [],
                'results_processed': 0,
                'error': str(e)
            }

    def search_domain(self, domain: str, engines: List[str] = None) -> Dict:
        """
        Search for emails related to a domain using multiple search engines.
        
        Args:
            domain: Domain to search for
            engines: List of search engines to use
            
        Returns:
            Dictionary with search results
        """
        if engines is None:
            engines = list(self.search_engines.keys())
            
        logger.info(f"Starting search for emails related to: {domain}")
        logger.info(f"Using search engines: {', '.join(engines)}")
        
        self.stats['start_time'] = datetime.now()
        self.stats['domains_searched'] = 1
        
        all_emails = set()
        search_results = {}
        
        for engine in engines:
            if engine not in self.search_engines:
                logger.warning(f"Skipping unknown search engine: {engine}")
                continue
                
            # Search with current engine
            result = self.search_engine(domain, engine)
            search_results[engine] = result
            
            if result['error']:
                self.stats['errors'] += 1
                logger.error(f"Error with {engine}: {result['error']}")
            else:
                all_emails.update(result['emails'])
                
            # Rate limiting
            if engine != engines[-1]:  # Don't delay after the last engine
                time.sleep(self.delay)
                
        # Update statistics
        self.stats['emails_found'] = len(all_emails)
        self.stats['unique_emails'] = len(all_emails)
        self.stats['end_time'] = datetime.now()
        
        # Store results
        self.all_emails = all_emails
        self.domain_emails[domain] = list(all_emails)
        self.search_results[domain] = search_results
        
        logger.info(f"Search completed. Found {len(all_emails)} unique emails")
        
        return {
            'domain': domain,
            'emails': list(all_emails),
            'search_results': search_results,
            'stats': self.stats.copy()
        }

    def export_results(self, output_file: str, format_type: str = 'txt') -> None:
        """
        Export results to file.
        
        Args:
            output_file: Output file path
            format_type: Output format (txt, csv, json)
        """
        try:
            if format_type == 'txt':
                self._export_txt(output_file)
            elif format_type == 'csv':
                self._export_csv(output_file)
            elif format_type == 'json':
                self._export_json(output_file)
            else:
                logger.error(f"Unsupported format: {format_type}")
                return
                
            logger.info(f"Results exported to {output_file}")
            
        except Exception as e:
            logger.error(f"Error exporting results: {e}")

    def _export_txt(self, output_file: str) -> None:
        """Export results to text file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Search Engine Email Checker Results\n")
            f.write("===================================\n\n")
            
            f.write(f"Domains Searched: {self.stats['domains_searched']}\n")
            f.write(f"Emails Found: {self.stats['emails_found']}\n")
            f.write(f"Unique Emails: {self.stats['unique_emails']}\n")
            f.write(f"Errors: {self.stats['errors']}\n")
            
            if self.stats['start_time'] and self.stats['end_time']:
                duration = self.stats['end_time'] - self.stats['start_time']
                f.write(f"Duration: {duration}\n")
            
            f.write("\nAll Email Addresses Found:\n")
            f.write("------------------------------\n")
            
            for email in sorted(self.all_emails):
                f.write(f"{email}\n")
            
            f.write("\nEmails by Domain:\n")
            f.write("------------------------------\n")
            
            for domain, emails in self.domain_emails.items():
                f.write(f"\n{domain}:\n")
                for email in sorted(emails):
                    f.write(f"  {email}\n")

    def _export_csv(self, output_file: str) -> None:
        """Export results to CSV file."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Email', 'Domain', 'Email_Domain'])
            
            for domain, emails in self.domain_emails.items():
                for email in emails:
                    email_domain = email.split('@')[1] if '@' in email else ''
                    writer.writerow([email, domain, email_domain])

    def _export_json(self, output_file: str) -> None:
        """Export results to JSON file."""
        data = {
            'domains': [
                {
                    'domain': domain,
                    'emails': emails,
                    'search_results': self.search_results.get(domain, {}),
                    'error': None
                }
                for domain, emails in self.domain_emails.items()
            ],
            'all_emails': list(self.all_emails),
            'domain_emails': self.domain_emails,
            'stats': self.stats
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

    def print_results(self) -> None:
        """Print results to console."""
        print("\n🔍 Starting search engine email extraction")
        print(f"📋 Domains: {', '.join(self.domain_emails.keys())}")
        print("=" * 60)
        
        print(f"\n📊 SEARCH RESULTS:")
        print(f"   Domains searched: {self.stats['domains_searched']}")
        print(f"   Emails found: {self.stats['emails_found']}")
        print(f"   Unique emails: {self.stats['unique_emails']}")
        print(f"   Errors: {self.stats['errors']}")
        
        if self.stats['start_time'] and self.stats['end_time']:
            duration = self.stats['end_time'] - self.stats['start_time']
            print(f"   Duration: {duration}")
        
        print("=" * 60)
        
        if self.all_emails:
            print(f"\n📧 EMAIL ADDRESSES FOUND ({len(self.all_emails)}):")
            print("-" * 40)
            
            for i, email in enumerate(sorted(self.all_emails), 1):
                print(f"  {i:2d}. {email}")
        else:
            print("\n❌ No email addresses found")

def show_banner():
    """Display tool banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Search Engine Email Checker and Extractor                ║
║                                                                              ║
║  Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com                ║
║  Version: 2.0.1.202510210253                                                  ║
║                                                                              ║
║  This tool searches for email addresses related to a domain using:          ║
║  • Google, DuckDuckGo, and Yahoo search engines                             ║
║  • Advanced email pattern matching and validation                           ║
║  • Duplicate detection and removal                                          ║
║  • Respectful searching with rate limiting                                  ║
║  • Comprehensive reporting and export capabilities                          ║
║                                                                              ║
║  USAGE EXAMPLES:                                                             ║
║  ──────────────────────────────────────────────────────────────────────────  ║
║  Basic:        python3 search_email_checker.py example.com                  ║
║  With output:  python3 search_email_checker.py example.com --output emails.txt ║
║  CSV export:   python3 search_email_checker.py example.com --output emails.csv --format csv ║
║  Specific:     python3 search_email_checker.py example.com --engines google,duckduckgo ║
║                                                                              ║
║  SECURITY NOTE: Use responsibly and in accordance with applicable laws      ║
║  and regulations. Always obtain proper authorization before testing.        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Search Engine Email Checker and Extractor - Email Discovery from Search Engines\n\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search engine email extraction
  python search_email_checker.py example.com
  
  # Multiple domains
  python search_email_checker.py example.com google.com github.com
  
  # With output file
  python search_email_checker.py example.com --output emails.txt
  
  # Export in different formats
  python search_email_checker.py example.com --output results.json --format json
  python search_email_checker.py example.com --output results.csv --format csv
  
  # Use specific search engines
  python search_email_checker.py example.com --engines google,duckduckgo

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
        """
    )
    
    parser.add_argument('domains', nargs='*', help='Domain(s) to search for email addresses')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', choices=['txt', 'csv', 'json'], default='txt',
                       help='Output format (default: txt)')
    parser.add_argument('--engines', default='google,duckduckgo,yahoo',
                       help='Comma-separated list of search engines (default: google,duckduckgo,yahoo)')
    parser.add_argument('--delay', type=float, default=2.0,
                       help='Delay between requests in seconds (default: 2.0)')
    parser.add_argument('--timeout', type=int, default=10,
                       help='Request timeout in seconds (default: 10)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--banner', action='store_true',
                       help='Show tool banner and exit')
    
    args = parser.parse_args()
    
    if args.banner:
        show_banner()
        return
    
    if not args.domains:
        print("Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")
        parser.error("At least one domain is required")
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Parse search engines
    engines = [engine.strip().lower() for engine in args.engines.split(',')]
    valid_engines = ['google', 'duckduckgo', 'yahoo']
    engines = [engine for engine in engines if engine in valid_engines]
    
    if not engines:
        print("Error: No valid search engines specified")
        return
    
    # Initialize checker
    checker = SearchEmailChecker(delay=args.delay, timeout=args.timeout)
    
    # Process each domain
    for domain in args.domains:
        try:
            result = checker.search_domain(domain, engines)
            
            if result['emails']:
                logger.info(f"Found {len(result['emails'])} emails for {domain}")
            else:
                logger.warning(f"No emails found for {domain}")
                
        except Exception as e:
            logger.error(f"Error processing domain {domain}: {e}")
            checker.stats['errors'] += 1
    
    # Print results
    checker.print_results()
    
    # Export results if requested
    if args.output:
        checker.export_results(args.output, args.format)

if __name__ == '__main__':
    main()

