# Email Enumeration Runner Script

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The Email Enumeration Runner Script (`run_enumeration.sh`) orchestrates the main email discovery workflow. It runs the core email-finding tools sequentially and merges their outputs into a single, deduplicated list.

## Features

- **Tool Orchestration**: Runs multiple discovery tools in sequence
- **Output Merging**: Deduplicates and sorts all results
- **Multiple Output Formats**: TXT, CSV, JSON
- **Progress and Summary**: Clear status output and final summary
- **Silent Mode**: Results-only output with `--silent`
- **Auto-Retry**: Re-runs a tool once if it exits with a non-zero code

## Prerequisites

- Shared venv created by `./installer.sh`
- Tool-specific setup scripts as needed:
  - `./scripts/setup_whois.sh`
  - `./scripts/setup_search.sh`
  - `./scripts/setup_gpg.sh`
  - `./scripts/setup_emailharvester.sh`
  - `./scripts/setup_theharvester.sh`

## Usage

```bash
./run_enumeration.sh <target> [options]
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output`, `-o` | Output file path | stdout only |
| `--format` | Output format: txt, csv, json | txt |
| `--max-depth` | Max crawl depth (web checker) | 3 |
| `--max-pages` | Max pages to crawl (web checker) | 20 |
| `--threads` | Web crawler threads | 3 |
| `--delay` | Delay between requests (seconds) | 1.0 |
| `--engines` | Search engines (comma-separated) | google,duckduckgo,yahoo |
| `--verbose`, `-v` | Verbose output (disables silent mode) | False |
| `--debug` | Debug output (disables silent mode) | False |
| `--silent` | Results only (still prints name + copyright) | True |
| `--banner` | Show banner and exit | - |
| `--help`, `-h` | Show help | - |

## Examples

### Basic Email Discovery
```bash
./run_enumeration.sh https://example.com
```

### CSV Output
```bash
./run_enumeration.sh example.com --output results.csv --format csv
```

### Limit Crawl Depth
```bash
./run_enumeration.sh example.com --max-depth 2 --max-pages 10
```

### Silent Mode (Default)
```bash
./run_enumeration.sh example.com --silent
```

### Verbose/Debug Mode
```bash
./run_enumeration.sh example.com --verbose
./run_enumeration.sh example.com --debug
```

## Tool Execution Order

1. **Web Email Checker** - Crawls websites for email addresses
2. **Whois Email Checker** - Extracts emails from whois data
3. **Search Engine Email Checker** - Searches Google, DuckDuckGo, Yahoo
4. **GPG/PGP Email Checker** - Searches GPG key servers
5. **EmailHarvester Checker** - Uses EmailHarvester
6. **TheHarvester Checker** - Uses TheHarvester

## Output

- **Console Output**: Summary and email list
- **File Output**: If `--output` is specified
- **Per-Run Temp/Logs**: Stored in `/tmp/email_finders_<pid>/`

## Notes

- Silent mode is the default.
- Use `--verbose` or `--debug` to see detailed status output.
- Some tools may require API keys or additional setup; use their setup scripts.
