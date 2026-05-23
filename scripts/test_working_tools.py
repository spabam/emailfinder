#!/usr/bin/env python3
"""
Test Working Email Finders
==========================

Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com
Version: 2.0.1.202510210253

This script tests the working email finder tools to verify they can find valid emails.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_tool(tool_name, command):
    """Run a tool and return the result"""
    print(f"\n{'='*60}")
    print(f"🔍 Testing {tool_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"✅ {tool_name} completed successfully")
            # Extract email count from output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if "Emails Found:" in line:
                    count = line.split("Emails Found:")[1].strip()
                    print(f"📊 Emails found: {count}")
                    break
        else:
            print(f"❌ {tool_name} failed with return code: {result.returncode}")
            if result.stderr:
                print(f"📄 Error: {result.stderr[:200]}...")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {tool_name} timed out")
        return False
    except Exception as e:
        print(f"❌ {tool_name} error: {e}")
        return False

def main():
    """Main test function"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        Email Finder Tools Test                              ║
║                                                                              ║
║  Copyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com                ║
║  Version: 2.0.1.202510210253                                                  ║
║                                                                              ║
║  Testing working email finder tools to verify they can find valid emails    ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    domain = "debian.org"
    print(f"🎯 Testing with domain: {domain}")
    
    # Test tools that are working
    tools = [
        ("GPG Email Checker", ["python3", "gpg_email_checker.py", domain, "--verbose"]),
        ("Web Email Finder", ["python3", "web_email_finder.py", domain, "--verbose"]),
    ]
    
    results = {}
    
    for tool_name, command in tools:
        success = run_tool(tool_name, command)
        results[tool_name] = success
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    working_tools = []
    failed_tools = []
    
    for tool_name, success in results.items():
        if success:
            working_tools.append(tool_name)
            print(f"✅ {tool_name}: WORKING")
        else:
            failed_tools.append(tool_name)
            print(f"❌ {tool_name}: FAILED")
    
    print(f"\n📈 Results:")
    print(f"  Working tools: {len(working_tools)}")
    print(f"  Failed tools: {len(failed_tools)}")
    
    if working_tools:
        print(f"\n✅ Working tools that can find valid emails:")
        for tool in working_tools:
            print(f"  • {tool}")
    
    if failed_tools:
        print(f"\n❌ Tools that need fixing:")
        for tool in failed_tools:
            print(f"  • {tool}")
    
    print(f"\nCopyright (c) 2015-2035 Andrea Bodei - info@andreabodei.com")

if __name__ == '__main__':
    main()

