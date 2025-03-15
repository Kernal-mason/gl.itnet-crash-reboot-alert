#!/usr/bin/env python3
"""
Test Script for Connectivity Monitor

Author: Mason Gonzalez
Created: March 2024
License: MIT
Repository: https://github.com/Kernal-mason/gl.itnet-crash-reboot-alert

This script tests the configuration and connectivity settings
before deploying the monitor. It verifies:
- Pushover credentials
- Target URL accessibility
- Basic connectivity

Usage:
    python3 test_connectivity.py
"""

import requests
import sys
from config import CONFIG

def test_configuration() -> bool:
    """
    Test configuration and connectivity settings.

    This function verifies:
    1. Pushover credentials are configured
    2. Target URL is accessible

    Returns:
        bool: True if all tests pass, False otherwise
    """
    print("Testing configuration...")
    
    # Test Pushover credentials
    if not CONFIG['PUSHOVER_TOKEN'] or not CONFIG['PUSHOVER_USER']:
        print("ERROR: Pushover credentials not configured")
        return False
    
    # Test target URL
    try:
        response = requests.get(CONFIG['TARGET_URL'], timeout=CONFIG['TIMEOUT'])
        response.raise_for_status()
        print(f"SUCCESS: Connected to {CONFIG['TARGET_URL']}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to connect to {CONFIG['TARGET_URL']}: {str(e)}")
        return False

if __name__ == "__main__":
    # Exit with status code based on test result
    sys.exit(0 if test_configuration() else 1) 
