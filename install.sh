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

# Installation script for connectivity monitor
INSTALL_DIR="/usr/bin"
LOG_DIR="/var/log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Copy scripts to installation directory
cp connectivity_monitor.py "$INSTALL_DIR/"
cp rotate_logs.sh "$INSTALL_DIR/"

# Set permissions
chmod +x "$INSTALL_DIR/connectivity_monitor.py"
chmod +x "$INSTALL_DIR/rotate_logs.sh"

# Create and set permissions for log file
touch "$LOG_DIR/connectivity.log"
chmod 644 "$LOG_DIR/connectivity.log"

# Copy example environment file
cp .env.example .env

echo "Installation complete. Please edit .env with your configuration." 
