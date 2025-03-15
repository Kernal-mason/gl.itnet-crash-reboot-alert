#!/bin/sh
#
# Installation Script for Connectivity Monitor
#
# Author: Mason Gonzalez
# Created: March 2024
# License: MIT
#
# This script handles the installation of the connectivity monitor
# and sets up necessary permissions and configurations.

# Installation directories for GL-iNet/BusyBox systems
INSTALL_DIR="/usr/bin"
LOG_DIR="/var/log"
CRON_DIR="/etc/crontabs"

# Create required directories
mkdir -p "$LOG_DIR"
mkdir -p "$CRON_DIR"

# Copy scripts to installation directory
cp connectivity_monitor.py "$INSTALL_DIR/"
cp rotate_logs.sh "$INSTALL_DIR/"

# Set permissions
chmod +x "$INSTALL_DIR/connectivity_monitor.py"
chmod +x "$INSTALL_DIR/rotate_logs.sh"

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

# Copy example environment file
cp .env.example .env

# Restart crond to apply changes
/etc/init.d/cron restart

echo "Installation complete. Please edit .env with your configuration."
echo "Cron jobs have been added to: $CRON_FILE" 
