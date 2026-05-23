# Test Working Email Finders

**Copyright (c) 2025-2035 Andrea Bodei**  
**Email: info@andreabodei.com**

## Overview

The Test Working Email Finders (`test_working_tools.py`) is a testing and validation script that verifies the functionality of all email finder tools in the suite. It runs each tool against test domains to ensure they can successfully find valid email addresses.

## Features

### Core Capabilities
- **Tool Validation**: Tests all email finder tools in the suite
- **Functionality Verification**: Ensures tools can find valid emails
- **Performance Testing**: Measures tool execution time and success rates
- **Error Detection**: Identifies tools with issues or failures
- **Comprehensive Reporting**: Provides detailed test results and statistics

### Advanced Features
- **Automated Testing**: Runs all tools automatically with minimal user intervention
- **Timeout Management**: Prevents tools from hanging with configurable timeouts
- **Result Analysis**: Analyzes tool output for email discovery success
- **Error Handling**: Robust error handling with detailed error reporting
- **Test Reporting**: Generates comprehensive test reports

## Installation

### Prerequisites
- Python 3.6 or higher
- All email finder tools installed and configured
- Internet connectivity for testing

### Dependencies
- All email finder Python scripts
- Required Python packages for each tool
- Test domains for validation

## Usage

### Basic Usage
```bash
python3 test_working_tools.py
```

### Advanced Usage
```bash
python3 test_working_tools.py [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--verbose` | Verbose output | False |
| `--timeout` | Timeout per tool (seconds) | 120 |
| `--test-domain` | Test domain to use | httpbin.org |

## Examples

### Basic Testing
```bash
python3 test_working_tools.py
```

### Verbose Testing
```bash
python3 test_working_tools.py --verbose
```

### Custom Timeout
```bash
python3 test_working_tools.py --timeout 300
```

### Custom Test Domain
```bash
python3 test_working_tools.py --test-domain example.com
```

## Tested Tools

### Email Finder Tools
1. **Email Checker** (`email_checker.py`)
2. **Whois Email Checker** (`whois_email_checker.py`)
3. **Search Email Checker** (`search_email_checker.py`)
4. **GPG Email Checker** (`gpg_email_checker.py`)
5. **EmailHarvester Checker** (`emailharvester_checker.py`)
6. **TheHarvester Checker** (`theharvester_checker.py`)
7. **Web Email Finder** (`web_email_finder.py`)

### Test Process
- **Tool Execution**: Runs each tool with test domain
- **Output Analysis**: Analyzes tool output for email discovery
- **Success Validation**: Verifies tools can find valid emails
- **Error Detection**: Identifies tools with issues
- **Performance Measurement**: Measures execution time

## Output

### Test Results
- **Tool Status**: Success/failure status for each tool
- **Email Count**: Number of emails found by each tool
- **Execution Time**: Time taken by each tool
- **Error Messages**: Detailed error information for failed tools
- **Overall Statistics**: Summary of all test results

### Report Contents
- **Test Summary**: Overview of all test results
- **Tool Performance**: Individual tool performance metrics
- **Error Analysis**: Detailed analysis of any failures
- **Recommendations**: Suggestions for tool improvements

## Configuration

### Default Settings
- **Test Domain**: httpbin.org (known to have test emails)
- **Timeout**: 120 seconds per tool
- **Verbose Mode**: Off by default
- **Test Scope**: All available email finder tools

### Customization
- Configure test domains for specific testing scenarios
- Adjust timeout values for slow tools
- Enable verbose mode for detailed debugging
- Select specific tools for testing

## Security Considerations

### Legal Notice
This tool is intended for testing purposes only. Users must:
- Use only authorized test domains
- Comply with all applicable laws and regulations
- Respect rate limits and usage policies
- Use responsibly and ethically

### Best Practices
- Use only authorized test domains
- Respect tool rate limits during testing
- Monitor test execution and results
- Follow responsible testing practices

## Troubleshooting

### Common Issues

1. **Tool Not Found**
   ```
   Error: Tool not found
   ```
   **Solution**: Ensure all email finder tools are installed and accessible

2. **Test Timeout**
   ```
   Error: Test timed out
   ```
   **Solution**: Increase timeout value or check tool performance

3. **No Emails Found**
   ```
   Warning: No emails found
   ```
   **Solution**: Check test domain or tool configuration

## Performance

### Optimization Tips
- Use appropriate timeout values for tool testing
- Monitor test execution and performance
- Use reliable test domains for consistent results
- Consider tool-specific optimization

### Resource Usage
- **Memory**: ~50-200MB depending on tools tested
- **CPU**: Moderate usage during tool execution
- **Network**: Varies based on tools and test domain
- **Storage**: Minimal, only for test results

## Integration

### Script Integration
```python
import subprocess
import json

# Run test suite
result = subprocess.run([
    'python3', 'test_working_tools.py',
    '--verbose'
], capture_output=True, text=True)

# Parse results
print("Test Results:")
print(result.stdout)
```

## Examples

### Comprehensive Testing
```bash
#!/bin/bash
# Comprehensive email finder testing

echo "Starting comprehensive email finder testing..."

python3 test_working_tools.py \
    --verbose \
    --timeout 300 \
    --test-domain httpbin.org

echo "Testing completed!"
```

### Custom Test Suite
```bash
#!/bin/bash
# Custom test suite with multiple domains

TEST_DOMAINS=("httpbin.org" "example.com" "test.com")

for domain in "${TEST_DOMAINS[@]}"; do
    echo "Testing with domain: $domain"
    python3 test_working_tools.py \
        --test-domain "$domain" \
        --timeout 180
done
```

## License

This software is provided "as is" without warranty of any kind. Use at your own risk.

**Copyright (c) 2025-2035 Andrea Bodei - All rights reserved.**
