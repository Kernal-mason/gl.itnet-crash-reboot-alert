#!/bin/sh
#
# Installation Script for Connectivity Monitor
#
# Author: Mason Gonzalez
# Created: March 2024
# License: MIT
# Repository: https://github.com/Kernal-mason/gl.itnet-crash-reboot-alert
#
# This script handles the installation of the connectivity monitor
# and sets up necessary permissions and configurations.

# Function to get user input for notification type
setup_notifications() {
    echo "Please choose your notification service:"
    echo "1) Pushover"
    echo "2) Telegram"
    read -p "Enter choice (1 or 2): " choice

    case $choice in
        1)
            echo "You selected Pushover"
            echo "Please follow these steps to configure Pushover:"
            echo "1. Create an account at https://pushover.net"
            echo "2. Create a new application to get your API token"
            echo "3. Get your user key from your account dashboard"
            echo ""
            echo "Update your .env file with:"
            echo "NOTIFICATION_TYPE=pushover"
            echo "PUSHOVER_TOKEN=your_api_token"
            echo "PUSHOVER_USER=your_user_key"
            ;;
        2)
            echo "You selected Telegram"
            echo "Please follow these steps to configure Telegram:"
            echo "1. Create a new bot using @BotFather on Telegram"
            echo "2. Get your bot token from BotFather"
            echo "3. Send a message to your bot"
            echo "4. Get your chat ID by visiting:"
            echo "   https://api.telegram.org/bot<YourBOTToken>/getUpdates"
            echo ""
            echo "Update your .env file with:"
            echo "NOTIFICATION_TYPE=telegram"
            echo "TELEGRAM_BOT_TOKEN=your_bot_token"
            echo "TELEGRAM_CHAT_ID=your_chat_id"
            ;;
        *)
            echo "Invalid choice. Defaulting to Pushover"
            ;;
    esac
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure it before running this script."
    exit 1
fi

# Run notification setup
setup_notifications

# Installation directories for GL-iNet/BusyBox systems
INSTALL_DIR="/usr/bin"
LOG_DIR="/var/log"
CRON_DIR="/etc/crontabs"

# Create required directories
mkdir -p "$LOG_DIR"
mkdir -p "$CRON_DIR"

# Copy environment file to installation directory
cp .env "$INSTALL_DIR/"

# Copy scripts to installation directory
cp connectivity_monitor.py "$INSTALL_DIR/"
cp rotate_logs.sh "$INSTALL_DIR/"

# Set permissions
chmod +x "$INSTALL_DIR/connectivity_monitor.py"
chmod +x "$INSTALL_DIR/rotate_logs.sh"
chmod 600 "$INSTALL_DIR/.env"

# Create and set permissions for log file
touch "$LOG_DIR/connectivity.log"
chmod 644 "$LOG_DIR/connectivity.log"

# Set up cron job if it doesn't exist
CRON_FILE="$CRON_DIR/root"
CRON_ENTRY="*/5 * * * * $INSTALL_DIR/connectivity_monitor.py"
ROTATE_ENTRY="0 0 * * * $INSTALL_DIR/rotate_logs.sh"

if [ ! -f "$CRON_FILE" ]; then
    touch "$CRON_FILE"
    chmod 600 "$CRON_FILE"
fi

if ! grep -q "$CRON_ENTRY" "$CRON_FILE"; then
    echo "$CRON_ENTRY" >> "$CRON_FILE"
    echo "$ROTATE_ENTRY" >> "$CRON_FILE"
fi

# Restart crond to apply changes
/etc/init.d/cron restart

echo "Installation complete."
echo "Cron jobs have been added to: $CRON_FILE"
echo "Environment file has been installed to: $INSTALL_DIR/.env" 
