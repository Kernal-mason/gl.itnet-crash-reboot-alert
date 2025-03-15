"""
Notification Module for Connectivity Monitor

Handles sending notifications via Pushover or Telegram.
"""

import requests
import logging
from typing import Optional
from config import CONFIG

def send_pushover_notification(message: str, priority: int = 0) -> bool:
    """Send notification via Pushover"""
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
        return True
    except Exception as e:
        logging.error(f"Failed to send Pushover notification: {str(e)}")
        return False

def send_telegram_notification(message: str, priority: int = 0) -> bool:
    """Send notification via Telegram"""
    try:
        # Add priority indicator to message
        priority_prefix = "🔴" if priority > 0 else "ℹ️"
        formatted_message = f"{priority_prefix} {message}"
        
        response = requests.post(
            f"https://api.telegram.org/bot{CONFIG['TELEGRAM_BOT_TOKEN']}/sendMessage",
            data={
                "chat_id": CONFIG['TELEGRAM_CHAT_ID'],
                "text": formatted_message,
                "parse_mode": "HTML"
            },
            timeout=CONFIG['TIMEOUT']
        )
        response.raise_for_status()
        logging.info("Telegram notification sent successfully")
        return True
    except Exception as e:
        logging.error(f"Failed to send Telegram notification: {str(e)}")
        return False

def send_notification(message: str, priority: int = 0) -> bool:
    """Send notification using configured method"""
    if CONFIG['NOTIFICATION_TYPE'].lower() == 'telegram':
        return send_telegram_notification(message, priority)
    else:
        return send_pushover_notification(message, priority) 
