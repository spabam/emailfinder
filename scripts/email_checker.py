#!/usr/bin/env python3
"""
Email Checker and Web Crawler
=============================

Copyright (c) 2015-2035 Andrea Bodei
Email: info@andreabodei.com
Version: 2.0.1.202510210253

This tool is designed to crawl websites and extract email addresses from all pages.
It provides comprehensive email discovery capabilities for legitimate purposes such as
contact information gathering, security assessments, and compliance checking.

WHAT THIS TOOL DOES:
===================
1. Crawls websites starting from a given URL
2. Follows internal links to discover all pages
3. Extracts email addresses using advanced regex patterns
4. Validates and deduplicates email addresses
5. Outputs results in organized, sorted lists
6. Provides comprehensive reporting and statistics

SECURITY USE CASES:
==================
- Security assessments and penetration testing
- Contact information gathering for legitimate purposes
- Compliance checking and data discovery
- Website content analysis and auditing
- Email address inventory and management

FEATURES:
=========
- Multi-threaded crawling for improved performance
- Advanced email pattern matching
- Duplicate detection and removal
- Domain filtering and validation
- Respectful crawling with rate limiting
- Comprehensive reporting and statistics
- Export capabilities (text, CSV, JSON)

USAGE EXAMPLES:
==============
Basic usage:
    python3 email_checker.py https://example.com

With depth limit:
    python3 email_checker.py https://example.com --max-depth 3

With domain restriction:
    python3 email_checker.py https://example.com --domain example.com

With output file:
    python3 email_checker.py https://example.com --output emails.txt

With threading:
    python3 email_checker.py https://example.com --threads 5

SECURITY CONSIDERATIONS:
=======================
- This tool is designed for legitimate security assessments and research
- Respects robots.txt and implements rate limiting
- Only crawls publicly accessible content
- Use responsibly and in accordance with applicable laws and regulations
- Always obtain proper authorization before testing

REQUIREMENTS:
============
- Python 3.6+
- requests library
- beautifulsoup4 library
- urllib3 library
- Internet connection

LICENSE:
========
This tool is provided as-is for educational and security assessment purposes.
Use responsibly and in accordance with applicable laws and regulations.
"""

import requests
import re
import argparse
import sys
import logging
import time
import json
import csv
from typing import Set, List, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import threading
from queue import Queue
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailChecker:
    """
    Email Checker and Web Crawler Class
    
    This class provides functionality to:
    - Crawl websites and discover all pages
    - Extract email addresses using advanced patterns
    - Validate and deduplicate email addresses
    - Generate comprehensive reports
    """
    
    def __init__(self, max_depth: int = 5, max_pages: int = 100, 
                 threads: int = 3, delay: float = 1.0, 
                 respect_robots: bool = True, domain_filter: str = None):
        """
        Initialize the Email Checker
        
        Args:
            max_depth: Maximum crawling depth (default: 5)
            max_pages: Maximum number of pages to crawl (default: 100)
            threads: Number of threads for concurrent crawling (default: 3)
            delay: Delay between requests in seconds (default: 1.0)
            respect_robots: Whether to respect robots.txt (default: True)
            domain_filter: Restrict crawling to specific domain (default: None)
        """
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.threads = threads
        self.delay = delay
        self.respect_robots = respect_robots
        self.domain_filter = domain_filter
        
        # Initialize session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Web-Email-Scraper/1.0 (Educational Tool)'
        })
        
        # Email patterns for extraction
        self.email_patterns = [
            # Standard email pattern
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            # Email with obfuscation patterns
            r'\b[A-Za-z0-9._%+-]+\s*\[at\]\s*[A-Za-z0-9.-]+\s*\[dot\]\s*[A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.\s*[A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%+-]+\s*\(at\)\s*[A-Za-z0-9.-]+\s*\(dot\)\s*[A-Z|a-z]{2,}\b',
            # Email in mailto links
            r'mailto:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            # Email in JavaScript
            r'["\']([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})["\']',
        ]
        
        # Compile regex patterns
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.email_patterns]
        
        # Crawling state
        self.visited_urls = set()
        self.to_visit = Queue()
        self.emails_found = set()
        self.url_emails = defaultdict(set)  # URL -> set of emails
        self.stats = {
            'pages_crawled': 0,
            'emails_found': 0,
            'unique_emails': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Threading
        self.lock = threading.Lock()
        self.robots_cache = {}
    
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
        
        # Remove mailto: prefix
        if email.startswith('mailto:'):
            email = email[7:]
        
        # Remove quotes and brackets
        email = re.sub(r'["\'<>]', '', email)
        
        # Remove extra whitespace
        email = email.strip()
        
        return email.lower()
    
    def extract_emails_from_text(self, text: str) -> Set[str]:
        """
        Extract email addresses from text using multiple patterns
        
        Args:
            text: Text content to search
            
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
    
    def get_robots_parser(self, base_url: str) -> Optional[RobotFileParser]:
        """
        Get robots.txt parser for domain
        
        Args:
            base_url: Base URL to check robots.txt for
            
        Returns:
            RobotFileParser instance or None
        """
        if not self.respect_robots:
            return None
        
        parsed_url = urlparse(base_url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        if domain in self.robots_cache:
            return self.robots_cache[domain]
        
        try:
            robots_url = urljoin(domain, '/robots.txt')
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            self.robots_cache[domain] = rp
            return rp
        except Exception as e:
            logger.warning(f"Could not read robots.txt for {domain}: {e}")
            self.robots_cache[domain] = None
            return None
    
    def can_fetch(self, url: str) -> bool:
        """
        Check if URL can be fetched according to robots.txt
        
        Args:
            url: URL to check
            
        Returns:
            True if URL can be fetched, False otherwise
        """
        if not self.respect_robots:
            return True
        
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        rp = self.get_robots_parser(domain)
        if rp is None:
            return True
        
        return rp.can_fetch(self.session.headers.get('User-Agent', '*'), url)
    
    def is_same_domain(self, url: str, base_domain: str) -> bool:
        """
        Check if URL belongs to the same domain
        
        Args:
            url: URL to check
            base_domain: Base domain to compare against
            
        Returns:
            True if same domain, False otherwise
        """
        if not self.domain_filter:
            return True
        
        parsed_url = urlparse(url)
        url_domain = parsed_url.netloc.lower()
        base_domain = base_domain.lower()
        
        return url_domain == base_domain or url_domain.endswith('.' + base_domain)
    
    def normalize_url(self, url: str, base_url: str) -> str:
        """
        Normalize URL for consistent comparison
        
        Args:
            url: URL to normalize
            base_url: Base URL for relative URL resolution
            
        Returns:
            Normalized URL
        """
        # Convert relative URLs to absolute
        if url.startswith('//'):
            url = urlparse(base_url).scheme + ':' + url
        elif url.startswith('/'):
            parsed_base = urlparse(base_url)
            url = f"{parsed_base.scheme}://{parsed_base.netloc}{url}"
        elif not url.startswith(('http://', 'https://')):
            url = urljoin(base_url, url)
        
        # Parse and reconstruct URL to normalize
        parsed = urlparse(url)
        
        # Remove fragment
        normalized = urlunparse((
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path,
            parsed.params,
            parsed.query,
            ''  # Remove fragment
        ))
        
        return normalized
    
    def extract_links(self, html: str, base_url: str) -> Set[str]:
        """
        Extract links from HTML content
        
        Args:
            html: HTML content
            base_url: Base URL for relative link resolution
            
        Returns:
            Set of extracted links
        """
        links = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract links from <a> tags
            for link in soup.find_all('a', href=True):
                href = link['href']
                normalized_url = self.normalize_url(href, base_url)
                
                # Filter URLs
                if (self.is_same_domain(normalized_url, self.domain_filter) and
                    normalized_url not in self.visited_urls and
                    self.can_fetch(normalized_url)):
                    links.add(normalized_url)
            
        except Exception as e:
            logger.warning(f"Error extracting links from {base_url}: {e}")
        
        return links
    
    def crawl_page(self, url: str) -> Tuple[Set[str], Set[str]]:
        """
        Crawl a single page and extract emails and links
        
        Args:
            url: URL to crawl
            
        Returns:
            Tuple of (emails_found, links_found)
        """
        emails = set()
        links = set()
        
        try:
            logger.info(f"Crawling: {url}")
            response = self.session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            # Extract emails from page content
            emails = self.extract_emails_from_text(response.text)
            
            # Extract links for further crawling
            links = self.extract_links(response.text, url)
            
            # Update statistics
            with self.lock:
                self.stats['pages_crawled'] += 1
                self.stats['emails_found'] += len(emails)
                self.url_emails[url] = emails
                self.emails_found.update(emails)
                self.stats['unique_emails'] = len(self.emails_found)
            
            logger.info(f"Found {len(emails)} emails, {len(links)} links on {url}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error crawling {url}: {e}")
            with self.lock:
                self.stats['errors'] += 1
        except Exception as e:
            logger.error(f"Unexpected error crawling {url}: {e}")
            with self.lock:
                self.stats['errors'] += 1
        
        return emails, links
    
    def worker_thread(self):
        """
        Worker thread for crawling pages
        """
        while True:
            try:
                # Get URL and depth from queue
                url, depth = self.to_visit.get(timeout=1)
                
                # Check if we've reached limits
                with self.lock:
                    if (self.stats['pages_crawled'] >= self.max_pages or
                        depth > self.max_depth):
                        self.to_visit.task_done()
                        continue
                
                # Crawl the page
                emails, links = self.crawl_page(url)
                
                # Add new links to queue if within depth limit
                if depth < self.max_depth:
                    for link in links:
                        if link not in self.visited_urls:
                            self.to_visit.put((link, depth + 1))
                
                # Mark task as done
                self.to_visit.task_done()
                
                # Rate limiting
                time.sleep(self.delay)
                
            except:
                break
    
    def crawl_website(self, start_url: str) -> Dict:
        """
        Crawl website starting from given URL
        
        Args:
            start_url: Starting URL for crawling
            
        Returns:
            Dictionary with crawling results and statistics
        """
        logger.info(f"Starting crawl of {start_url}")
        self.stats['start_time'] = datetime.now()
        
        # Parse domain filter
        if not self.domain_filter:
            parsed_url = urlparse(start_url)
            self.domain_filter = parsed_url.netloc
        
        # Add starting URL to queue
        self.to_visit.put((start_url, 0))
        
        # Start worker threads
        threads = []
        for i in range(self.threads):
            thread = threading.Thread(target=self.worker_thread)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Process queue
        while not self.to_visit.empty():
            try:
                url, depth = self.to_visit.get(timeout=1)
                
                # Check limits
                if (self.stats['pages_crawled'] >= self.max_pages or
                    depth > self.max_depth):
                    self.to_visit.task_done()
                    continue
                
                # Mark as visited
                self.visited_urls.add(url)
                
                # Crawl page
                emails, links = self.crawl_page(url)
                
                # Add new links to queue
                if depth < self.max_depth:
                    for link in links:
                        if link not in self.visited_urls:
                            self.to_visit.put((link, depth + 1))
                
                self.to_visit.task_done()
                time.sleep(self.delay)
                
            except:
                break
        
        # Wait for all tasks to complete
        self.to_visit.join()
        
        self.stats['end_time'] = datetime.now()
        
        # Prepare results
        results = {
            'emails': sorted(list(self.emails_found)),
            'url_emails': dict(self.url_emails),
            'stats': self.stats,
            'visited_urls': list(self.visited_urls)
        }
        
        return results
    
    def export_results(self, results: Dict, output_file: str, format: str = 'txt'):
        """
        Export results to file
        
        Args:
            results: Crawling results
            output_file: Output file path
            format: Export format ('txt', 'csv', 'json')
        """
        try:
            if format == 'txt':
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("Web Email Scraper Results\n")
                    f.write("=" * 50 + "\n\n")
                    
                    f.write(f"Website: {results['stats'].get('start_url', 'N/A')}\n")
                    f.write(f"Pages Crawled: {results['stats']['pages_crawled']}\n")
                    f.write(f"Emails Found: {results['stats']['emails_found']}\n")
                    f.write(f"Unique Emails: {results['stats']['unique_emails']}\n")
                    f.write(f"Errors: {results['stats']['errors']}\n\n")
                    
                    f.write("Email Addresses Found:\n")
                    f.write("-" * 30 + "\n")
                    for email in results['emails']:
                        f.write(f"{email}\n")
                    
                    f.write(f"\nEmails by URL:\n")
                    f.write("-" * 30 + "\n")
                    for url, emails in results['url_emails'].items():
                        if emails:
                            f.write(f"\n{url}:\n")
                            for email in sorted(emails):
                                f.write(f"  {email}\n")
            
            elif format == 'csv':
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Email', 'URL', 'Domain'])
                    
                    for url, emails in results['url_emails'].items():
                        for email in emails:
                            domain = email.split('@')[1] if '@' in email else ''
                            writer.writerow([email, url, domain])
            
            elif format == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Results exported to {output_file}")
            
        except Exception as e:
            logger.error(f"Error exporting results: {e}")

def print_banner():
    """
    Print the tool banner and manifest with usage instructions.
    """
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        Email Checker and Web Crawler                        ║
║                                                                              ║
║  Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com                     ║
║  Version: 2.0.1.202510210253                                                  ║
║                                                                              ║
║  This tool crawls websites and extracts email addresses from all pages:     ║
║  • Multi-threaded crawling for improved performance                         ║
║  • Advanced email pattern matching and validation                           ║
║  • Duplicate detection and removal                                          ║
║  • Respectful crawling with rate limiting                                   ║
║  • Comprehensive reporting and export capabilities                          ║
║                                                                              ║
║  USAGE EXAMPLES:                                                             ║
║  ──────────────────────────────────────────────────────────────────────────  ║
║  Basic:        python3 email_checker.py https://example.com             ║
║  With depth:   python3 email_checker.py https://example.com --max-depth 3 ║
║  With output:  python3 email_checker.py https://example.com --output emails.txt ║
║  With threads: python3 email_checker.py https://example.com --threads 5 ║
║                                                                              ║
║  SECURITY NOTE: Use responsibly and in accordance with applicable laws      ║
║  and regulations. Always obtain proper authorization before testing.        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """
    Main function that handles command line arguments and orchestrates the email scraping process.
    """
    parser = argparse.ArgumentParser(
        description='Web Email Scraper and Crawler - Email Discovery Tool\n\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic crawling
  python email_checker.py https://example.com
  
  # With depth limit
  python email_checker.py https://example.com --max-depth 3
  
  # With domain restriction
  python email_checker.py https://example.com --domain example.com
  
  # With output file
  python email_checker.py https://example.com --output emails.txt
  
  # With threading and rate limiting
  python email_checker.py https://example.com --threads 5 --delay 0.5
  
  # Export in different formats
  python email_checker.py https://example.com --output results.json --format json
  python email_checker.py https://example.com --output results.csv --format csv

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
        """
    )
    
    parser.add_argument('url', nargs='?', help='Starting URL to crawl')
    parser.add_argument('--max-depth', '-d', type=int, default=5, 
                       help='Maximum crawling depth (default: 5)')
    parser.add_argument('--max-pages', '-p', type=int, default=100,
                       help='Maximum number of pages to crawl (default: 100)')
    parser.add_argument('--threads', '-t', type=int, default=3,
                       help='Number of threads for concurrent crawling (default: 3)')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--domain', help='Restrict crawling to specific domain')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', choices=['txt', 'csv', 'json'], default='txt',
                       help='Output format (default: txt)')
    parser.add_argument('--no-robots', action='store_true',
                       help='Do not respect robots.txt')
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
    if not args.url and not args.banner:
        print("Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")
        parser.error("URL is required unless using --banner option")
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create checker instance
    checker = EmailChecker(
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        threads=args.threads,
        delay=args.delay,
        respect_robots=not args.no_robots,
        domain_filter=args.domain
    )
    
    # Check if URL has a scheme, if not try both HTTP and HTTPS
    if not args.url.startswith(('http://', 'https://')):
        print(f"🔍 Starting email scraping of {args.url}")
        print(f"📊 Max depth: {args.max_depth}, Max pages: {args.max_pages}")
        print(f"🧵 Threads: {args.threads}, Delay: {args.delay}s")
        print("=" * 60)
        print("🌐 No scheme provided, trying both HTTP and HTTPS...")
        
        # Try both HTTP and HTTPS
        https_url = f"https://{args.url}"
        http_url = f"http://{args.url}"
        
        all_emails = set()
        all_url_emails = {}
        combined_stats = {
            'pages_crawled': 0,
            'emails_found': 0,
            'unique_emails': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Try HTTPS first (more common for modern sites)
        print(f"\n🔒 Trying HTTPS: {https_url}")
        try:
            https_results = checker.crawl_website(https_url)
            all_emails.update(https_results['emails'])
            all_url_emails.update(https_results['url_emails'])
            combined_stats['pages_crawled'] += https_results['stats']['pages_crawled']
            combined_stats['emails_found'] += https_results['stats']['emails_found']
            combined_stats['errors'] += https_results['stats']['errors']
            if not combined_stats['start_time']:
                combined_stats['start_time'] = https_results['stats']['start_time']
            if https_results['emails']:
                print(f"✅ HTTPS found {len(https_results['emails'])} emails")
            else:
                print("❌ HTTPS found no emails")
        except Exception as e:
            print(f"❌ HTTPS failed: {e}")
            combined_stats['errors'] += 1
        
        # Try HTTP as well (some sites only support HTTP or have different content)
        print(f"\n🔓 Trying HTTP: {http_url}")
        try:
            # Create a new checker instance for HTTP
            http_checker = EmailChecker(
                max_depth=args.max_depth,
                max_pages=args.max_pages,
                threads=args.threads,
                delay=args.delay,
                respect_robots=not args.no_robots,
                domain_filter=args.domain
            )
            http_results = http_checker.crawl_website(http_url)
            all_emails.update(http_results['emails'])
            all_url_emails.update(http_results['url_emails'])
            combined_stats['pages_crawled'] += http_results['stats']['pages_crawled']
            combined_stats['emails_found'] += http_results['stats']['emails_found']
            combined_stats['errors'] += http_results['stats']['errors']
            if not combined_stats['start_time']:
                combined_stats['start_time'] = http_results['stats']['start_time']
            if http_results['emails']:
                print(f"✅ HTTP found {len(http_results['emails'])} emails")
            else:
                print("❌ HTTP found no emails")
        except Exception as e:
            print(f"❌ HTTP failed: {e}")
            combined_stats['errors'] += 1
        
        # Set end time
        combined_stats['end_time'] = datetime.now()
        combined_stats['unique_emails'] = len(all_emails)
        
        # Create combined results
        results = {
            'emails': sorted(list(all_emails)),
            'url_emails': all_url_emails,
            'stats': combined_stats,
            'visited_urls': list(set().union(*[checker.visited_urls, http_checker.visited_urls if 'http_checker' in locals() else set()]))
        }
        
    else:
        # URL already has a scheme, proceed normally
        print(f"🔍 Starting email scraping of {args.url}")
        print(f"📊 Max depth: {args.max_depth}, Max pages: {args.max_pages}")
        print(f"🧵 Threads: {args.threads}, Delay: {args.delay}s")
        print("=" * 60)
        
        try:
            results = checker.crawl_website(args.url)
        except Exception as e:
            logger.error(f"Error during crawling: {e}")
            sys.exit(1)
    
    # Display results
    print(f"\n📊 CRAWLING RESULTS:")
    print(f"   Pages crawled: {results['stats']['pages_crawled']}")
    print(f"   Emails found: {results['stats']['emails_found']}")
    print(f"   Unique emails: {results['stats']['unique_emails']}")
    print(f"   Errors: {results['stats']['errors']}")
    
    if results['stats']['start_time'] and results['stats']['end_time']:
        duration = results['stats']['end_time'] - results['stats']['start_time']
        print(f"   Duration: {duration}")
    
    print("=" * 60)
    
    if results['emails']:
        print(f"\n📧 EMAIL ADDRESSES FOUND ({len(results['emails'])}):")
        print("-" * 40)
        for i, email in enumerate(results['emails'], 1):
            print(f"{i:3d}. {email}")
    else:
        print("\n❌ No email addresses found")
    
    # Export results if requested
    if args.output:
        checker.export_results(results, args.output, args.format)

if __name__ == '__main__':
    main()
