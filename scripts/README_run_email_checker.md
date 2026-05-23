# Email Checker Runner Script

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The Email Checker Runner Script (`run_email_checker.sh`) is a bash wrapper script that activates the Email Checker virtual environment and runs the email checker tool with all provided command line arguments. It provides a convenient interface for running the email checker with proper environment setup.

## Features

### Core Capabilities
- **Virtual Environment Management**: Activates the Email Checker virtual environment
- **Argument Passing**: Passes through all command line arguments to the Python script
- **Environment Validation**: Checks if the virtual environment exists
- **Error Handling**: Provides clear error messages for common issues
- **Convenient Interface**: Simple command-line interface for tool execution

### Advanced Features
- **Environment Setup**: Automatically sets up the required environment
- **Dependency Management**: Ensures all required dependencies are available
- **Path Resolution**: Handles path resolution for the Python script
- **Exit Code Handling**: Proper exit code handling and error reporting

## Installation

### Prerequisites
- Bash shell
- Python 3.6 or higher
- Virtual environment setup (if using virtual environments)

### Dependencies
- Email Checker Python script (`email_checker.py`)
- Required Python packages in virtual environment

## Usage

### Basic Usage
```bash
./run_email_checker.sh <url>
```

### Advanced Usage
```bash
./run_email_checker.sh <url> [options]
```

### Command Line Options

All command line options are passed through to the underlying Python script. See the Email Checker documentation for available options.

## Examples

### Basic Web Crawling
```bash
./run_email_checker.sh https://example.com
```

### Advanced Configuration
```bash
./run_email_checker.sh https://example.com --max-depth 3 --output emails.txt
```

### Custom Output
```bash
./run_email_checker.sh https://example.com --output custom_emails.txt --format csv
```

### Verbose Output
```bash
./run_email_checker.sh https://example.com --verbose
```

## Script Workflow

### Execution Flow
1. **Environment Check**: Verifies virtual environment exists
2. **Environment Activation**: Activates the virtual environment
3. **Script Execution**: Runs the email checker with provided arguments
4. **Result Handling**: Processes and returns results

### Error Handling
- **Environment Issues**: Clear error messages for environment problems
- **Script Failures**: Proper error handling for script execution failures
- **Argument Validation**: Validates arguments before passing to Python script

## Configuration

### Default Settings
- **Virtual Environment**: Uses default virtual environment path
- **Python Script**: Uses default script path
- **Argument Passing**: Passes all arguments to underlying script

### Customization
- Modify virtual environment path if needed
- Adjust Python script path if relocated
- Customize error handling and logging

## Security Considerations

### Legal Notice
This tool is intended for authorized security testing only. Users must:
- Obtain proper authorization before crawling websites
- Comply with website terms of service and robots.txt
- Respect rate limits and server resources
- Use responsibly and ethically

### Best Practices
- Always check robots.txt before crawling
- Use appropriate delays to avoid overwhelming servers
- Respect website terms of service
- Only crawl websites you own or have permission to test

## Troubleshooting

### Common Issues

1. **Virtual Environment Not Found**
   ```
   Error: Virtual environment not found
   ```
   **Solution**: Ensure virtual environment is properly set up

2. **Permission Denied**
   ```
   Error: Permission denied
   ```
   **Solution**: Check script permissions
   ```bash
   chmod +x run_email_checker.sh
   ```

3. **Python Script Not Found**
   ```
   Error: Python script not found
   ```
   **Solution**: Ensure email_checker.py is in the correct location

## Performance

### Optimization Tips
- Ensure virtual environment is properly configured
- Use appropriate arguments for the underlying script
- Monitor system resources during execution
- Consider using the script directly for advanced configurations

### Resource Usage
- **Memory**: Minimal overhead, depends on underlying script
- **CPU**: Low overhead, depends on underlying script
- **Network**: Depends on underlying script usage
- **Storage**: Minimal, only for script execution

## Integration

### Script Integration
```bash
#!/bin/bash
# Integration with other scripts

TARGET="https://example.com"
OUTPUT_DIR="./email_results"

# Run email checker
./run_email_checker.sh "$TARGET" \
    --output "$OUTPUT_DIR/emails.txt" \
    --format txt

# Process results
process_email_results "$OUTPUT_DIR/emails.txt"
```

## Examples

### Automated Email Discovery
```bash
#!/bin/bash
# Automated email discovery using email checker

TARGETS=("https://example.com" "https://google.com" "https://github.com")
OUTPUT_DIR="./automated_results"

for target in "${TARGETS[@]}"; do
    echo "Crawling $target for emails..."
    ./run_email_checker.sh "$target" \
        --output "$OUTPUT_DIR/$(basename $target)_emails.txt" \
        --format txt
done
```

### Batch Processing
```bash
#!/bin/bash
# Batch processing with email checker

while IFS= read -r url; do
    echo "Processing $url..."
    ./run_email_checker.sh "$url" \
        --output "./results/$(basename $url)_emails.txt"
done < urls.txt
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**
