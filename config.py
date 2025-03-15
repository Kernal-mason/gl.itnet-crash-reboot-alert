"""
Configuration Module for Connectivity Monitor

Author: Mason Gonzalez
Created: March 2024
License: MIT
Repository: https://github.com/Kernal-mason/gl.itnet-crash-reboot-alert

This module manages the configuration settings for the connectivity monitor,
loading values from environment variables with fallback to defaults.

Configuration values:
    NOTIFICATION_TYPE: Notification type ('pushover' or 'telegram')
    PUSHOVER_TOKEN: Pushover API token
    PUSHOVER_USER: Pushover user key
    TELEGRAM_BOT_TOKEN: Telegram bot token
    TELEGRAM_CHAT_ID: Telegram chat ID
    TARGET_URL: URL or IP to monitor
    TIMEOUT: Request timeout in seconds
    MAX_RETRIES: Number of retry attempts
    RETRY_DELAY: Delay between retries in seconds
    LOG_PATH: Path to log file
"""

import os
from typing import Dict, Any

# Default configuration with type hints
DEFAULT_CONFIG: Dict[str, Any] = {
    'NOTIFICATION_TYPE': 'pushover',  # 'pushover' or 'telegram'
    'PUSHOVER_TOKEN': '',  # Pushover API token
    'PUSHOVER_USER': '',   # Pushover user key
    'TELEGRAM_BOT_TOKEN': '',  # Telegram bot token
    'TELEGRAM_CHAT_ID': '',    # Telegram chat ID
    'TARGET_URL': 'https://example.com',  # Target URL to monitor
    'TIMEOUT': 5,    # Request timeout in seconds
    'MAX_RETRIES': 3,  # Number of retry attempts
    'RETRY_DELAY': 15,  # Delay between retries in seconds
    'LOG_PATH': '/var/log/connectivity.log'  # Log file path
}

# Load configuration from environment variables with defaults
CONFIG = {
    key: os.getenv(key, DEFAULT_CONFIG[key])
    for key in DEFAULT_CONFIG
}

# Convert numeric values to integers
CONFIG['TIMEOUT'] = int(CONFIG['TIMEOUT'])
CONFIG['MAX_RETRIES'] = int(CONFIG['MAX_RETRIES'])
CONFIG['RETRY_DELAY'] = int(CONFIG['RETRY_DELAY']) 
