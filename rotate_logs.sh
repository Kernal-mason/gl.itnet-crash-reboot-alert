#!/bin/sh
#
# Log Rotation Script for Connectivity Monitor
#
# Author: Mason Gonzalez
# Created: March 2024
# License: MIT
#
# This script handles log rotation for the connectivity monitor
# on systems with limited storage capacity.

# Simple log rotation script for busybox systems
MAX_SIZE=1048576  # 1MB in bytes
LOG_FILE="/var/log/connectivity.log"

# Check if log file exists and is larger than MAX_SIZE
if [ -f "$LOG_FILE" ] && [ $(stat -c%s "$LOG_FILE") -gt $MAX_SIZE ]; then
    mv "$LOG_FILE" "$LOG_FILE.old"
    touch "$LOG_FILE"
    chmod 644 "$LOG_FILE"
fi 
