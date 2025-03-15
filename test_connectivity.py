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
import os
from config import CONFIG

def test_file_permissions() -> bool:
    """Test file permissions and paths"""
    try:
        # Test log file permissions
        log_dir = os.path.dirname(CONFIG['LOG_PATH'])
        if not os.access(log_dir, os.W_OK):
            print(f"ERROR: Cannot write to log directory: {log_dir}")
            return False
        
        # Test reboot access
        if not os.access('/sbin/reboot', os.X_OK):
            print("WARNING: May not have permission to execute reboot")
        
        return True
    except Exception as e:
        print(f"ERROR: Permission test failed: {str(e)}")
        return False

def test_cron_setup() -> bool:
    """Test cron configuration"""
    try:
        if not os.path.exists('/etc/crontabs/root'):
            print("ERROR: Cron configuration not found")
            return False
        
        with open('/etc/crontabs/root', 'r') as f:
            content = f.read()
            if 'connectivity_monitor.py' not in content:
                print("ERROR: Cron job not configured")
                return False
        
        return True
    except Exception as e:
        print(f"ERROR: Cron test failed: {str(e)}")
        return False

def test_configuration() -> bool:
    """
    Test configuration and connectivity settings.

    This function verifies:
    1. Notification credentials are configured
    2. Target URL is accessible
    3. File permissions
    4. Cron setup

    Returns:
        bool: True if all tests pass, False otherwise
    """
    print("Testing configuration...")
    
    print("\n1. Testing notification credentials...")
    notification_type = CONFIG['NOTIFICATION_TYPE'].lower()
    
    if notification_type == 'pushover':
        if not CONFIG['PUSHOVER_TOKEN'] or not CONFIG['PUSHOVER_USER']:
            print("ERROR: Pushover credentials not configured")
            return False
        print("SUCCESS: Pushover credentials found")
    elif notification_type == 'telegram':
        if not CONFIG['TELEGRAM_BOT_TOKEN'] or not CONFIG['TELEGRAM_CHAT_ID']:
            print("ERROR: Telegram credentials not configured")
            return False
        print("SUCCESS: Telegram credentials found")
    else:
        print(f"ERROR: Invalid notification type: {notification_type}")
        return False

    print("\n2. Testing target URL...")
    try:
        response = requests.get(CONFIG['TARGET_URL'], timeout=CONFIG['TIMEOUT'])
        response.raise_for_status()
        print(f"SUCCESS: Connected to {CONFIG['TARGET_URL']}")
    except Exception as e:
        print(f"ERROR: Failed to connect to {CONFIG['TARGET_URL']}: {str(e)}")
        return False

    print("\n3. Testing file permissions...")
    if not test_file_permissions():
        return False

    print("\n4. Testing cron setup...")
    if not test_cron_setup():
        return False

    print("\nAll tests passed successfully!")
    return True

if __name__ == "__main__":
    # Exit with status code based on test result
    sys.exit(0 if test_configuration() else 1) 
