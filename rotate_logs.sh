#!/bin/sh
#
# Log Rotation Script for Connectivity Monitor
#
# Author: Mason Gonzalez
# Created: March 2024
# License: MIT
# Repository: https://github.com/Kernal-mason/gl.itnet-crash-reboot-alert
#
# This script handles log rotation for the connectivity monitor
# on systems with limited storage capacity.

# Simple log rotation script for busybox systems
MAX_SIZE=524288  # 512KB in bytes - adjusted for router storage
LOG_FILE="/var/log/connectivity.log"

# Check if log file exists and is larger than MAX_SIZE
if [ -f "$LOG_FILE" ] && [ $(busybox stat -c%s "$LOG_FILE") -gt $MAX_SIZE ]; then
    mv "$LOG_FILE" "$LOG_FILE.old"
    touch "$LOG_FILE"
    chmod 644 "$LOG_FILE"
fi 
