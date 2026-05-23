#!/bin/bash
# Email Enumeration Runner Script
# ===============================
#
# Copyright (c) 2015-2035 Andrea Bodei
# Email: info@andreabodei.com
# Version: 2.0.1.202510210253
#
# This script runs the email finding tools sequentially and merges their
# outputs into a single, ordered, unique list of email addresses.
#
# WHAT THIS SCRIPT DOES:
# =====================
# 1. Runs the Web Email Checker (email_checker.py) to crawl websites
# 2. Runs the Whois Email Checker (whois_email_checker.py) to extract from whois
# 3. Runs the Search Engine Email Checker (search_email_checker.py) to search Google, DuckDuckGo, Yahoo
# 4. Runs the GPG/PGP Email Checker (gpg_email_checker.py) to search GPG key servers
# 5. Runs the EmailHarvester Email Checker (emailharvester_checker.py) to use EmailHarvester
# 6. Runs the TheHarvester Email Checker (theharvester_checker.py) to use TheHarvester
# 7. Merges all found emails into a single, deduplicated, sorted list
# 8. Provides comprehensive reporting and statistics
# 9. Exports results in multiple formats (text, CSV, JSON)
#
# USAGE:
# ======
# ./run_enumeration.sh <target> [options]
#
# EXAMPLES:
# =========
# ./run_enumeration.sh https://example.com
# ./run_enumeration.sh example.com
# ./run_enumeration.sh https://example.com --output all_emails.txt
# ./run_enumeration.sh example.com --output results.csv --format csv
# ./run_enumeration.sh --help
#
# REQUIREMENTS:
# ============
# - All email finder tools must be set up using their respective setup scripts
# - Virtual environments must be configured
# - whois command-line tool must be installed
# - Internet connection for search engine queries
#
# LICENSE:
# ========
# This script is provided as-is for educational and security assessment purposes.
# Use responsibly and in accordance with applicable laws and regulations.

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/scripts"

# Default values
OUTPUT_FILE=""
OUTPUT_FORMAT="txt"
VERBOSE=false
DEBUG=false
SILENT=true
MAX_DEPTH=3
MAX_PAGES=20
THREADS=3
DELAY=1.0
SEARCH_ENGINES="google,duckduckgo,yahoo"

# Temporary files
TEMP_DIR="/tmp/email_finders_$$"
WEB_EMAILS_FILE="$TEMP_DIR/web_emails.txt"
WHOIS_EMAILS_FILE="$TEMP_DIR/whois_emails.txt"
SEARCH_EMAILS_FILE="$TEMP_DIR/search_emails.txt"
MERGED_EMAILS_FILE="$TEMP_DIR/merged_emails.txt"

# Statistics
WEB_EMAILS_COUNT=0
WHOIS_EMAILS_COUNT=0
SEARCH_EMAILS_COUNT=0
GPG_EMAILS_COUNT=0
EMAILHARVESTER_EMAILS_COUNT=0
THEHARVESTER_EMAILS_COUNT=0
TOTAL_EMAILS_COUNT=0
UNIQUE_EMAILS_COUNT=0
START_TIME=$(date +%s)

# Progress tracking (silent mode only)
TOTAL_STEPS=6
CURRENT_STEP=0
PROGRESS_WIDTH=24

# Function to print colored output
print_status() {
    if [ "$SILENT" = true ]; then
        return
    fi
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    if [ "$SILENT" = true ]; then
        return
    fi
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    if [ "$SILENT" = true ]; then
        return
    fi
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    if [ "$SILENT" = true ]; then
        return
    fi
    echo -e "${PURPLE}$1${NC}"
}

print_result_header() {
    echo -e "${PURPLE}$1${NC}"
}

maybe_blank_line() {
    if [ "$SILENT" != true ]; then
        echo ""
    fi
}

progress_init() {
    if [ "$SILENT" != true ]; then
        return
    fi
    printf "Progress: [%s] %d%%" "$(printf '%*s' "$PROGRESS_WIDTH" "" | tr ' ' '-')" 0
}

progress_update() {
    if [ "$SILENT" != true ]; then
        return
    fi
    CURRENT_STEP=$((CURRENT_STEP + 1))
    if [ "$CURRENT_STEP" -gt "$TOTAL_STEPS" ]; then
        CURRENT_STEP="$TOTAL_STEPS"
    fi
    local filled=$((CURRENT_STEP * PROGRESS_WIDTH / TOTAL_STEPS))
    local empty=$((PROGRESS_WIDTH - filled))
    local bar_filled
    local bar_empty
    bar_filled="$(printf '%*s' "$filled" "" | tr ' ' '#')"
    bar_empty="$(printf '%*s' "$empty" "" | tr ' ' '-')"
    local percent=$((CURRENT_STEP * 100 / TOTAL_STEPS))
    printf "\rProgress: [%s%s] %d%%" "$bar_filled" "$bar_empty" "$percent"
    if [ "$CURRENT_STEP" -eq "$TOTAL_STEPS" ]; then
        echo ""
    fi
}

# Function to show usage
show_usage() {
    echo "Email Enumeration Runner Script"
    echo "================================"
    echo ""
    echo "Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com"
    echo ""
    echo "This script runs the email finding tools and merges their outputs."
    echo ""
    echo "USAGE:"
    echo "  $0 <target> [options]"
    echo ""
    echo "ARGUMENTS:"
    echo "  target                 URL or domain to analyze"
    echo ""
    echo "OPTIONS:"
    echo "  --output, -o FILE      Output file path (default: stdout)"
    echo "  --format FORMAT        Output format: txt, csv, json (default: txt)"
    echo "  --max-depth N          Maximum crawling depth for web checker (default: 3)"
    echo "  --max-pages N          Maximum pages to crawl (default: 20)"
    echo "  --threads N            Number of threads for web crawling (default: 3)"
    echo "  --delay N              Delay between requests in seconds (default: 1.0)"
    echo "  --engines ENGINES      Comma-separated search engines (default: google,duckduckgo,yahoo)"
    echo "  --verbose, -v          Enable verbose output (disables silent mode)"
    echo "  --debug                Enable debug output (disables silent mode)"
    echo "  --silent               Suppress all progress output; show results only (default)"
    echo "  --help, -h             Show this help message"
    echo ""
    echo "EXAMPLES:"
    echo "  $0 https://example.com"
    echo "  $0 example.com"
    echo "  $0 https://example.com --output all_emails.txt"
    echo "  $0 example.com --output results.csv --format csv"
    echo "  $0 https://example.com --max-depth 2 --max-pages 10"
    echo ""
    echo "TOOLS USED:"
    echo "  1. Web Email Checker - Crawls websites for email addresses"
    echo "  2. Whois Email Checker - Extracts emails from whois data"
    echo "  3. Search Engine Email Checker - Searches Google, DuckDuckGo, Yahoo"
    echo ""
    echo "OUTPUT:"
    echo "  Merged, deduplicated, and sorted list of all found email addresses"
    echo ""
}

# Function to cleanup temporary files
cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}

# Use shared venv in home directory (outside Dropbox)
VENV_DIR="${RALPHCODE_VENV_DIR:-$HOME/.venv}"
VENV_BIN="$VENV_DIR/bin"
VENV_PY="$VENV_BIN/python"

# Function to check if virtual environment exists
check_virtual_envs() {
    if [ ! -d "$VENV_DIR" ]; then
        print_error "Shared virtual environment not found at: $VENV_DIR"
        print_error "Please run the setup scripts first:"
        print_error "  ./installer.sh"
        print_error "  ./scripts/setup_whois.sh"
        print_error "  ./scripts/setup_search.sh"
        print_error "  ./scripts/setup_gpg.sh"
        print_error "  ./scripts/setup_emailharvester.sh"
        print_error "  ./scripts/setup_theharvester.sh"
        exit 1
    fi

    if [ ! -x "$VENV_PY" ]; then
        print_error "Python not found in virtual environment: $VENV_PY"
        print_error "Please run the setup scripts first:"
        print_error "  ./installer.sh"
        print_error "  ./scripts/setup_whois.sh"
        print_error "  ./scripts/setup_search.sh"
        print_error "  ./scripts/setup_gpg.sh"
        print_error "  ./scripts/setup_emailharvester.sh"
        print_error "  ./scripts/setup_theharvester.sh"
        exit 1
    fi
}

# Run a tool inside the shared venv and capture output to a log file
run_tool_with_log() {
    local log_file="$1"
    shift
    PATH="$VENV_BIN:$PATH" "$@" > "$log_file" 2>&1
}

# Function to extract domain from URL
extract_domain() {
    local target="$1"
    if [[ $target == http* ]]; then
        # Extract domain from URL
        echo "$target" | sed -E 's|^https?://([^/]+).*|\1|' | sed 's|:.*||'
    else
        # Already a domain
        echo "$target"
    fi
}

# Function to run web email checker
run_web_checker() {
    local target="$1"
    print_header "🔍 Running Web Email Checker..."
    
    if [ "$VERBOSE" = true ]; then
        print_status "Crawling: $target"
        print_status "Max depth: $MAX_DEPTH, Max pages: $MAX_PAGES"
        print_status "Threads: $THREADS, Delay: $DELAY"
    fi
    
    local log_file="$TEMP_DIR/web_checker.log"
    local retry_log="$TEMP_DIR/web_checker_retry.log"
    local attempt
    local exit_code=0

    WEB_EMAILS_COUNT=0

    for attempt in 1 2; do
        local current_log="$log_file"
        if [ "$attempt" -eq 2 ]; then
            current_log="$retry_log"
        fi

        rm -f "$WEB_EMAILS_FILE"
        run_tool_with_log "$current_log" \
            "$VENV_PY" "$SCRIPT_DIR/email_checker.py" "$target" \
            --max-depth "$MAX_DEPTH" \
            --max-pages "$MAX_PAGES" \
            --threads "$THREADS" \
            --delay "$DELAY" \
            --output "$WEB_EMAILS_FILE" \
            --format txt
        exit_code=$?

        if [ -f "$WEB_EMAILS_FILE" ]; then
            WEB_EMAILS_COUNT=$(grep -c "^[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}$" "$WEB_EMAILS_FILE" 2>/dev/null)
            [ -z "$WEB_EMAILS_COUNT" ] && WEB_EMAILS_COUNT=0
        else
            WEB_EMAILS_COUNT=0
        fi

        if [ "$exit_code" -eq 0 ]; then
            if [ "$WEB_EMAILS_COUNT" -gt 0 ]; then
                print_success "Web checker found $WEB_EMAILS_COUNT emails"
            else
                print_warning "Web checker found no emails"
            fi
            return
        fi

        if [ "$attempt" -eq 1 ]; then
            print_warning "Web checker failed (exit code $exit_code); retrying once..."
        fi
    done

    print_warning "Web checker failed (exit code $exit_code)"
    if [ "$VERBOSE" = true ] && [ "$SILENT" != true ]; then
        print_status "Log: $retry_log"
        tail -n 20 "$retry_log"
    fi
}

# Function to run whois email checker
run_whois_checker() {
    local target="$1"
    local domain=$(extract_domain "$target")
    
    print_header "🔍 Running Whois Email Checker..."
    
    if [ "$VERBOSE" = true ]; then
        print_status "Querying whois for: $domain"
    fi
    
    local log_file="$TEMP_DIR/whois_checker.log"
    local retry_log="$TEMP_DIR/whois_checker_retry.log"
    local attempt
    local exit_code=0

    WHOIS_EMAILS_COUNT=0

    for attempt in 1 2; do
        local current_log="$log_file"
        if [ "$attempt" -eq 2 ]; then
            current_log="$retry_log"
        fi

        rm -f "$WHOIS_EMAILS_FILE"
        run_tool_with_log "$current_log" \
            "$VENV_PY" "$SCRIPT_DIR/whois_email_checker.py" "$domain" \
            --output "$WHOIS_EMAILS_FILE" \
            --format txt
        exit_code=$?

        if [ -f "$WHOIS_EMAILS_FILE" ]; then
            WHOIS_EMAILS_COUNT=$(grep -c "^[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}$" "$WHOIS_EMAILS_FILE" 2>/dev/null)
            [ -z "$WHOIS_EMAILS_COUNT" ] && WHOIS_EMAILS_COUNT=0
        else
            WHOIS_EMAILS_COUNT=0
        fi

        if [ "$exit_code" -eq 0 ]; then
            if [ "$WHOIS_EMAILS_COUNT" -gt 0 ]; then
                print_success "Whois checker found $WHOIS_EMAILS_COUNT emails"
            else
                print_warning "Whois checker found no emails"
            fi
            return
        fi

        if [ "$attempt" -eq 1 ]; then
            print_warning "Whois checker failed (exit code $exit_code); retrying once..."
        fi
    done

    print_warning "Whois checker failed (exit code $exit_code)"
    if [ "$VERBOSE" = true ] && [ "$SILENT" != true ]; then
        print_status "Log: $retry_log"
        tail -n 20 "$retry_log"
    fi
}

# Function to run search email checker
run_search_checker() {
    local target="$1"
    local domain=$(extract_domain "$target")
    
    print_header "🔍 Running Search Engine Email Checker..."
    
    if [ "$VERBOSE" = true ]; then
        print_status "Searching engines: $SEARCH_ENGINES for: $domain"
    fi
    
    local log_file="$TEMP_DIR/search_checker.log"
    local retry_log="$TEMP_DIR/search_checker_retry.log"
    local attempt
    local exit_code=0

    SEARCH_EMAILS_COUNT=0

    for attempt in 1 2; do
        local current_log="$log_file"
        if [ "$attempt" -eq 2 ]; then
            current_log="$retry_log"
        fi

        rm -f "$SEARCH_EMAILS_FILE"
        run_tool_with_log "$current_log" \
            "$VENV_PY" "$SCRIPT_DIR/search_email_checker.py" "$domain" \
            --engines "$SEARCH_ENGINES" \
            --delay "$DELAY" \
            --output "$SEARCH_EMAILS_FILE" \
            --format txt
        exit_code=$?

        if [ -f "$SEARCH_EMAILS_FILE" ]; then
            SEARCH_EMAILS_COUNT=$(grep -c "^[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}$" "$SEARCH_EMAILS_FILE" 2>/dev/null)
            [ -z "$SEARCH_EMAILS_COUNT" ] && SEARCH_EMAILS_COUNT=0
        else
            SEARCH_EMAILS_COUNT=0
        fi

        if [ "$exit_code" -eq 0 ]; then
            if [ "$SEARCH_EMAILS_COUNT" -gt 0 ]; then
                print_success "Search checker found $SEARCH_EMAILS_COUNT emails"
            else
                print_warning "Search checker found no emails"
            fi
            return
        fi

        if [ "$attempt" -eq 1 ]; then
            print_warning "Search checker failed (exit code $exit_code); retrying once..."
        fi
    done

    print_warning "Search checker failed (exit code $exit_code)"
    if [ "$VERBOSE" = true ] && [ "$SILENT" != true ]; then
        print_status "Log: $retry_log"
        tail -n 20 "$retry_log"
    fi
}

# Function to run GPG email checker
run_gpg_checker() {
    local target="$1"
    local domain=$(extract_domain "$target")
    
    print_header "🔍 Running GPG/PGP Email Checker..."
    
    if [ "$VERBOSE" = true ]; then
        print_status "Searching GPG key servers for: $domain"
    fi

    local log_file="$TEMP_DIR/gpg_checker.log"
    local retry_log="$TEMP_DIR/gpg_checker_retry.log"
    local cmd=( "$VENV_PY" "$SCRIPT_DIR/gpg_email_checker.py" "$domain" --output "$TEMP_DIR/gpg_emails.txt" )
    local attempt
    local exit_code=0
    local count=0

    if [ "$SILENT" != true ]; then
        cmd+=(--verbose)
    fi

    for attempt in 1 2; do
        rm -f "$TEMP_DIR/gpg_emails.txt"
        if [ "$SILENT" = true ]; then
            if [ "$attempt" -eq 1 ]; then
                run_tool_with_log "$log_file" "${cmd[@]}"
            else
                run_tool_with_log "$retry_log" "${cmd[@]}"
            fi
            exit_code=$?
        else
            PATH="$VENV_BIN:$PATH" "${cmd[@]}"
            exit_code=$?
        fi

        if [ -f "$TEMP_DIR/gpg_emails.txt" ] && [ -s "$TEMP_DIR/gpg_emails.txt" ]; then
            count=$(grep -c "^[^#]" "$TEMP_DIR/gpg_emails.txt" 2>/dev/null)
        else
            count=0
        fi

        if [ "$exit_code" -eq 0 ]; then
            GPG_EMAILS_COUNT="$count"
            if [ "$count" -gt 0 ]; then
                print_success "GPG email checker found $count emails"
            else
                print_warning "GPG email checker found no emails"
            fi
            return
        fi

        if [ "$attempt" -eq 1 ]; then
            print_warning "GPG email checker failed (exit code $exit_code); retrying once..."
        fi
    done

    GPG_EMAILS_COUNT=0
    print_warning "GPG email checker failed (exit code $exit_code)"
}

# Function to run EmailHarvester email checker
run_emailharvester_checker() {
    local target="$1"
    local domain=$(extract_domain "$target")
    
    print_header "🔍 Running EmailHarvester Email Checker..."
    
    if [ "$VERBOSE" = true ]; then
        print_status "Using EmailHarvester for: $domain"
    fi

    local log_file="$TEMP_DIR/emailharvester_checker.log"
    local retry_log="$TEMP_DIR/emailharvester_checker_retry.log"
    local cmd=( "$VENV_PY" "$SCRIPT_DIR/emailharvester_checker.py" "$domain" --output "$TEMP_DIR/emailharvester_emails.txt" )
    local attempt
    local exit_code=0
    local count=0

    if [ "$SILENT" != true ]; then
        cmd+=(--verbose)
    fi

    for attempt in 1 2; do
        rm -f "$TEMP_DIR/emailharvester_emails.txt"
        if [ "$SILENT" = true ]; then
            if [ "$attempt" -eq 1 ]; then
                run_tool_with_log "$log_file" "${cmd[@]}"
            else
                run_tool_with_log "$retry_log" "${cmd[@]}"
            fi
            exit_code=$?
        else
            PATH="$VENV_BIN:$PATH" "${cmd[@]}"
            exit_code=$?
        fi

        if [ -f "$TEMP_DIR/emailharvester_emails.txt" ] && [ -s "$TEMP_DIR/emailharvester_emails.txt" ]; then
            count=$(grep -c "^[^#]" "$TEMP_DIR/emailharvester_emails.txt" 2>/dev/null)
        else
            count=0
        fi

        if [ "$exit_code" -eq 0 ]; then
            EMAILHARVESTER_EMAILS_COUNT="$count"
            if [ "$count" -gt 0 ]; then
                print_success "EmailHarvester checker found $count emails"
            else
                print_warning "EmailHarvester checker found no emails"
            fi
            return
        fi

        if [ "$attempt" -eq 1 ]; then
            print_warning "EmailHarvester checker failed (exit code $exit_code); retrying once..."
        fi
    done

    EMAILHARVESTER_EMAILS_COUNT=0
    print_warning "EmailHarvester checker failed (exit code $exit_code)"
}

# Function to run TheHarvester email checker
run_theharvester_checker() {
    local target="$1"
    local domain=$(extract_domain "$target")
    
    print_header "🔍 Running TheHarvester Email Checker..."
    
    if [ "$VERBOSE" = true ]; then
        print_status "Using TheHarvester for: $domain"
    fi

    local log_file="$TEMP_DIR/theharvester_checker.log"
    local retry_log="$TEMP_DIR/theharvester_checker_retry.log"
    local cmd=( "$VENV_PY" "$SCRIPT_DIR/theharvester_checker.py" "$domain" --output "$TEMP_DIR/theharvester_emails.txt" )
    local attempt
    local exit_code=0
    local count=0

    if [ "$SILENT" != true ]; then
        cmd+=(--verbose)
    fi

    for attempt in 1 2; do
        rm -f "$TEMP_DIR/theharvester_emails.txt"
        if [ "$SILENT" = true ]; then
            if [ "$attempt" -eq 1 ]; then
                run_tool_with_log "$log_file" "${cmd[@]}"
            else
                run_tool_with_log "$retry_log" "${cmd[@]}"
            fi
            exit_code=$?
        else
            PATH="$VENV_BIN:$PATH" "${cmd[@]}"
            exit_code=$?
        fi

        if [ -f "$TEMP_DIR/theharvester_emails.txt" ] && [ -s "$TEMP_DIR/theharvester_emails.txt" ]; then
            count=$(grep -c "^[^#]" "$TEMP_DIR/theharvester_emails.txt" 2>/dev/null)
        else
            count=0
        fi

        if [ "$exit_code" -eq 0 ]; then
            THEHARVESTER_EMAILS_COUNT="$count"
            if [ "$count" -gt 0 ]; then
                print_success "TheHarvester checker found $count emails"
            else
                print_warning "TheHarvester checker found no emails"
            fi
            return
        fi

        if [ "$attempt" -eq 1 ]; then
            print_warning "TheHarvester checker failed (exit code $exit_code); retrying once..."
        fi
    done

    THEHARVESTER_EMAILS_COUNT=0
    print_warning "TheHarvester checker failed (exit code $exit_code)"
}

# Function to merge and deduplicate emails
merge_emails() {
    print_header "🔄 Merging and deduplicating emails..."
    
    # Create temporary file for all emails
    local all_emails_file="$TEMP_DIR/all_emails.txt"
    > "$all_emails_file"
    
    # Extract emails from web checker output
    if [ -f "$WEB_EMAILS_FILE" ]; then
        grep "^[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}$" "$WEB_EMAILS_FILE" >> "$all_emails_file" 2>/dev/null
    fi
    
    # Extract emails from whois checker output
    if [ -f "$WHOIS_EMAILS_FILE" ]; then
        grep "^[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}$" "$WHOIS_EMAILS_FILE" >> "$all_emails_file" 2>/dev/null
    fi
    
    # Extract emails from search checker output
    if [ -f "$SEARCH_EMAILS_FILE" ]; then
        grep "^[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}$" "$SEARCH_EMAILS_FILE" >> "$all_emails_file" 2>/dev/null
    fi
    
    # Extract emails from GPG checker output
    if [ -f "$TEMP_DIR/gpg_emails.txt" ]; then
        grep "^[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}$" "$TEMP_DIR/gpg_emails.txt" >> "$all_emails_file" 2>/dev/null
    fi
    
    # Extract emails from EmailHarvester checker output
    if [ -f "$TEMP_DIR/emailharvester_emails.txt" ]; then
        grep "^[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}$" "$TEMP_DIR/emailharvester_emails.txt" >> "$all_emails_file" 2>/dev/null
    fi
    
    # Extract emails from TheHarvester checker output
    if [ -f "$TEMP_DIR/theharvester_emails.txt" ]; then
        grep "^[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}$" "$TEMP_DIR/theharvester_emails.txt" >> "$all_emails_file" 2>/dev/null
    fi
    
    # Count total emails before deduplication
    TOTAL_EMAILS_COUNT=$(wc -l < "$all_emails_file" 2>/dev/null)
    [ -z "$TOTAL_EMAILS_COUNT" ] && TOTAL_EMAILS_COUNT=0
    
    # Sort and deduplicate
    if [ -f "$all_emails_file" ] && [ -s "$all_emails_file" ]; then
        sort -u "$all_emails_file" > "$MERGED_EMAILS_FILE"
        UNIQUE_EMAILS_COUNT=$(wc -l < "$MERGED_EMAILS_FILE" 2>/dev/null)
        [ -z "$UNIQUE_EMAILS_COUNT" ] && UNIQUE_EMAILS_COUNT=0
        print_success "Merged $TOTAL_EMAILS_COUNT emails into $UNIQUE_EMAILS_COUNT unique emails"
    else
        UNIQUE_EMAILS_COUNT=0
        print_warning "No emails found to merge"
    fi
}

# Function to generate output
generate_output() {
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))
    
    print_result_header "📊 FINAL RESULTS"
    echo "============================================================"
    echo "Target: $TARGET"
    echo "Web Emails Found: $WEB_EMAILS_COUNT"
    echo "Whois Emails Found: $WHOIS_EMAILS_COUNT"
    echo "Search Emails Found: $SEARCH_EMAILS_COUNT"
    echo "GPG Emails Found: $GPG_EMAILS_COUNT"
    echo "EmailHarvester Emails Found: $EMAILHARVESTER_EMAILS_COUNT"
    echo "TheHarvester Emails Found: $THEHARVESTER_EMAILS_COUNT"
    echo "Total Emails: $TOTAL_EMAILS_COUNT"
    echo "Unique Emails: $UNIQUE_EMAILS_COUNT"
    echo "Duration: ${duration}s"
    echo "============================================================"
    
    if [ $UNIQUE_EMAILS_COUNT -gt 0 ]; then
        echo ""
        print_result_header "📧 EMAIL ADDRESSES FOUND ($UNIQUE_EMAILS_COUNT):"
        echo "----------------------------------------"
        
        if [ -f "$MERGED_EMAILS_FILE" ]; then
            local counter=1
            while IFS= read -r email; do
                printf "%3d. %s\n" "$counter" "$email"
                ((counter++))
            done < "$MERGED_EMAILS_FILE"
        fi
    else
        echo ""
        echo "❌ No email addresses found"
    fi
    
    # Export to file if requested
    if [ -n "$OUTPUT_FILE" ]; then
        export_to_file "$OUTPUT_FILE" "$OUTPUT_FORMAT"
    fi
}

# Function to export results to file
export_to_file() {
    local file="$1"
    local format="$2"
    
    print_status "Exporting results to $file (format: $format)"
    
    case "$format" in
        "txt")
            {
                echo "Email Enumeration Results"
                echo "========================="
                echo ""
                echo "Target: $TARGET"
                echo "Web Emails Found: $WEB_EMAILS_COUNT"
                echo "Whois Emails Found: $WHOIS_EMAILS_COUNT"
                echo "Search Emails Found: $SEARCH_EMAILS_COUNT"
                echo "GPG Emails Found: $GPG_EMAILS_COUNT"
                echo "EmailHarvester Emails Found: $EMAILHARVESTER_EMAILS_COUNT"
                echo "TheHarvester Emails Found: $THEHARVESTER_EMAILS_COUNT"
                echo "Total Emails: $TOTAL_EMAILS_COUNT"
                echo "Unique Emails: $UNIQUE_EMAILS_COUNT"
                echo "Duration: ${duration}s"
                echo ""
                echo "Email Addresses Found:"
                echo "----------------------"
                if [ -f "$MERGED_EMAILS_FILE" ]; then
                    cat "$MERGED_EMAILS_FILE"
                fi
            } > "$file"
            ;;
        "csv")
            {
                echo "Email,Source,Target"
                if [ -f "$MERGED_EMAILS_FILE" ]; then
                    while IFS= read -r email; do
                        # Determine source based on which file contains the email
                        local source=""
                        if [ -f "$WEB_EMAILS_FILE" ] && grep -q "^$email$" "$WEB_EMAILS_FILE" 2>/dev/null; then
                            source="Web"
                        fi
                        if [ -f "$WHOIS_EMAILS_FILE" ] && grep -q "^$email$" "$WHOIS_EMAILS_FILE" 2>/dev/null; then
                            if [ -n "$source" ]; then
                                source="Web,Whois"
                            else
                                source="Whois"
                            fi
                        fi
                        if [ -f "$SEARCH_EMAILS_FILE" ] && grep -q "^$email$" "$SEARCH_EMAILS_FILE" 2>/dev/null; then
                            if [ -n "$source" ]; then
                                source="$source,Search"
                            else
                                source="Search"
                            fi
                        fi
                        if [ -f "$TEMP_DIR/gpg_emails.txt" ] && grep -q "^$email$" "$TEMP_DIR/gpg_emails.txt" 2>/dev/null; then
                            if [ -n "$source" ]; then
                                source="$source,GPG"
                            else
                                source="GPG"
                            fi
                        fi
                        if [ -f "$TEMP_DIR/emailharvester_emails.txt" ] && grep -q "^$email$" "$TEMP_DIR/emailharvester_emails.txt" 2>/dev/null; then
                            if [ -n "$source" ]; then
                                source="$source,EmailHarvester"
                            else
                                source="EmailHarvester"
                            fi
                        fi
                        if [ -f "$TEMP_DIR/theharvester_emails.txt" ] && grep -q "^$email$" "$TEMP_DIR/theharvester_emails.txt" 2>/dev/null; then
                            if [ -n "$source" ]; then
                                source="$source,TheHarvester"
                            else
                                source="TheHarvester"
                            fi
                        fi
                        echo "$email,$source,$TARGET"
                    done < "$MERGED_EMAILS_FILE"
                fi
            } > "$file"
            ;;
        "json")
            {
                echo "{"
                echo "  \"target\": \"$TARGET\","
                echo "  \"web_emails_found\": $WEB_EMAILS_COUNT,"
                echo "  \"whois_emails_found\": $WHOIS_EMAILS_COUNT,"
                echo "  \"search_emails_found\": $SEARCH_EMAILS_COUNT,"
                echo "  \"gpg_emails_found\": $GPG_EMAILS_COUNT,"
                echo "  \"emailharvester_emails_found\": $EMAILHARVESTER_EMAILS_COUNT,"
                echo "  \"theharvester_emails_found\": $THEHARVESTER_EMAILS_COUNT,"
                echo "  \"total_emails\": $TOTAL_EMAILS_COUNT,"
                echo "  \"unique_emails\": $UNIQUE_EMAILS_COUNT,"
                echo "  \"duration_seconds\": $duration,"
                echo "  \"emails\": ["
                if [ -f "$MERGED_EMAILS_FILE" ]; then
                    local first=true
                    while IFS= read -r email; do
                        if [ "$first" = true ]; then
                            first=false
                        else
                            echo ","
                        fi
                        echo -n "    \"$email\""
                    done < "$MERGED_EMAILS_FILE"
                    echo ""
                fi
                echo "  ]"
                echo "}"
            } > "$file"
            ;;
    esac
    
    print_success "Results exported to $file"
}

# Function to show banner
show_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                         Email Enumeration Runner                           ║"
    echo "║                                                                              ║"
    echo "║  Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com                ║"
    echo "║  Version: 2.0.1.202510210253                                                  ║"
    echo "║                                                                              ║"
    echo "║  This script runs the email finding tools and merges their outputs:        ║"
    echo "║  • Web Email Checker - Crawls websites for email addresses                  ║"
    echo "║  • Whois Email Checker - Extracts emails from whois data                    ║"
    echo "║  • Search Engine Email Checker - Searches Google, DuckDuckGo, Yahoo        ║"
    echo "║  • GPG/PGP Email Checker - Searches GPG key servers for emails             ║"
    echo "║  • EmailHarvester Email Checker - Uses EmailHarvester for email discovery  ║"
    echo "║  • TheHarvester Email Checker - Uses TheHarvester for email discovery      ║"
    echo "║  • Merged, deduplicated, and sorted output                                  ║"
    echo "║  • Comprehensive reporting and statistics                                   ║"
    echo "║                                                                              ║"
    echo "║  USAGE: ./run_enumeration.sh <target> [options]                             ║"
    echo "║  Tip: use --silent for results-only output                                   ║"
    echo "║                                                                              ║"
    echo "║  SECURITY NOTE: Use responsibly and in accordance with applicable laws      ║"
    echo "║  and regulations. Always obtain proper authorization before testing.        ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Main execution
main() {
    # Set up trap for cleanup
    trap cleanup EXIT
    
    # Create temporary directory
    mkdir -p "$TEMP_DIR"
    
    # Parse command line arguments
    if [ $# -eq 0 ]; then
        show_usage
        exit 1
    fi
    
    TARGET=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --output|-o)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            --format)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            --max-depth)
                MAX_DEPTH="$2"
                shift 2
                ;;
            --max-pages)
                MAX_PAGES="$2"
                shift 2
                ;;
            --threads)
                THREADS="$2"
                shift 2
                ;;
            --delay)
                DELAY="$2"
                shift 2
                ;;
            --engines)
                SEARCH_ENGINES="$2"
                shift 2
                ;;
            --verbose|-v)
                VERBOSE=true
                SILENT=false
                shift
                ;;
            --debug)
                DEBUG=true
                VERBOSE=true
                SILENT=false
                shift
                ;;
            --silent)
                SILENT=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            --banner)
                show_banner
                exit 0
                ;;
            -*)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                if [ -z "$TARGET" ]; then
                    TARGET="$1"
                else
                    print_error "Multiple targets not supported. Please specify only one target."
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    if [ -z "$TARGET" ]; then
        print_error "Target is required"
        echo "Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com"
        show_usage
        exit 1
    fi
    
    # Validate output format
    if [[ ! "$OUTPUT_FORMAT" =~ ^(txt|csv|json)$ ]]; then
        print_error "Invalid output format: $OUTPUT_FORMAT. Must be txt, csv, or json."
        exit 1
    fi
    
    # Ensure verbose/debug always overrides silent
    if [ "$VERBOSE" = true ] || [ "$DEBUG" = true ]; then
        SILENT=false
    fi

    # Show banner unless silent
    if [ "$SILENT" = true ]; then
        echo "Email Enumeration Runner Script"
        echo "Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com"
        progress_init
    else
        show_banner
    fi
    
    # Check virtual environments
    check_virtual_envs
    
    print_status "Starting comprehensive email discovery for: $TARGET"
    maybe_blank_line
    
    # Run all email finders
    run_web_checker "$TARGET"
    progress_update
    maybe_blank_line
    run_whois_checker "$TARGET"
    progress_update
    maybe_blank_line
    run_search_checker "$TARGET"
    progress_update
    maybe_blank_line
    run_gpg_checker "$TARGET"
    progress_update
    maybe_blank_line
    run_emailharvester_checker "$TARGET"
    progress_update
    maybe_blank_line
    run_theharvester_checker "$TARGET"
    progress_update
    maybe_blank_line
    merge_emails
    maybe_blank_line
    generate_output
}

# Run main function
main "$@"
