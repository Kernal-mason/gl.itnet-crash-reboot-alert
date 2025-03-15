#!/usr/bin/env python3
"""
Connectivity Monitor

A script to monitor network connectivity and trigger system reboot on failure.
Designed for busybox-based systems with limited resources.

Author: Mason Gonzalez
Created: March 2024
License: MIT
Repository: https://github.com/Kernal-mason/gl.itnet-crash-reboot-alert

This script monitors network connectivity to a specified URL/IP and triggers
a system reboot if connectivity fails. It includes Pushover notifications
for alerts and comprehensive logging.

Typical usage:
    - Run directly: python3 connectivity_monitor.py
    - Via cron job: */5 * * * * /usr/bin/connectivity_monitor.py

Dependencies:
    - requests: For HTTP requests
    - python-dotenv: For environment variable management
    - Pushover account: For notifications
"""

import requests
import subprocess
import logging
import sys
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from config import CONFIG

# Initialize environment and logging
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG['LOG_PATH']),
        logging.StreamHandler(sys.stdout)
    ]
)

def send_pushover_notification(message: str, priority: int = 0) -> None:
    """
    Send notification via Pushover service.

    Args:
        message (str): The message to send
        priority (int): Message priority (-2 to 2)
            -2: Lowest priority
            -1: Low priority
             0: Normal priority
             1: High priority
             2: Emergency priority

    Raises:
        requests.exceptions.RequestException: If the notification fails to send
    """
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": CONFIG['PUSHOVER_TOKEN'],
                "user": CONFIG['PUSHOVER_USER'],
                "message": message,
                "priority": priority
            },
            timeout=CONFIG['TIMEOUT']
        )
        response.raise_for_status()
        logging.info("Pushover notification sent successfully")
    except Exception as e:
        logging.error(f"Failed to send Pushover notification: {str(e)}")

def check_connectivity() -> bool:
    """
    Check if the target URL/IP is reachable.

    The function will attempt to connect multiple times based on MAX_RETRIES
    configuration, with delays between attempts.

    Returns:
        bool: True if connection successful, False otherwise
    """
    for attempt in range(CONFIG['MAX_RETRIES']):
        try:
            response = requests.get(CONFIG['TARGET_URL'], timeout=CONFIG['TIMEOUT'])
            response.raise_for_status()
            logging.info(f"Successfully connected to {CONFIG['TARGET_URL']}")
            return True
        except Exception as e:
            error_message = f"Connectivity check failed (attempt {attempt + 1}/{CONFIG['MAX_RETRIES']}): {str(e)}"
            logging.error(error_message)
            if attempt < CONFIG['MAX_RETRIES'] - 1:
                logging.info(f"Waiting {CONFIG['RETRY_DELAY']} seconds before retry...")
                time.sleep(CONFIG['RETRY_DELAY'])
            else:
                send_pushover_notification(error_message, priority=1)
    return False

def reboot_system() -> None:
    """
    Reboot the system using the busybox reboot command.

    This function requires appropriate permissions to execute the reboot command.
    It will send a notification before attempting the reboot.

    Raises:
        subprocess.SubprocessError: If the reboot command fails
        SystemExit: With code 4 if reboot fails
    """
    try:
        logging.info("Initiating system reboot")
        send_pushover_notification(
            "System is being rebooted due to connectivity issues",
            priority=1
        )
        subprocess.run(['reboot'], check=True)
    except Exception as e:
        error_message = f"Failed to reboot system: {str(e)}"
        logging.error(error_message)
        send_pushover_notification(error_message, priority=2)
        sys.exit(4)

def main() -> None:
    """
    Main function that orchestrates the connectivity monitoring.

    The function will:
    1. Check connectivity to the target URL
    2. Attempt to reboot if connectivity fails
    3. Log all actions and send notifications

    Exit codes:
        0: Success
        1: General error
        4: Reboot failure
    """
    try:
        logging.info("Starting connectivity check")
        if not check_connectivity():
            reboot_system()
        
    except Exception as e:
        error_message = f"Script execution failed: {str(e)}"
        logging.error(error_message)
        send_pushover_notification(error_message, priority=2)
        sys.exit(1)

if __name__ == "__main__":
    main() 
