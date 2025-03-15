# Connectivity Monitor

Author: Mason Gonzalez
Created: March 2024
License: MIT

A Python script that monitors network connectivity and automatically reboots the system if connectivity fails, with Pushover notifications for alerts.

## Features

- Continuous monitoring of specified URL/IP
- Pushover notifications for connectivity failures and system events
- Automatic system reboot on connectivity failure
- Comprehensive logging to both file and stdout
- Error handling and timeout management

## Prerequisites

- Python 3.6 or higher
- Busybox-based Linux system
- Pushover account (for notifications)

## Installation

1. Install required Python package:
```bash
opkg update  # or your system's package manager
opkg install python3-pip
pip3 install -r requirements.txt
```

2. Clone or copy the script:
```bash
cp connectivity_monitor.py /usr/bin/
chmod +x /usr/bin/connectivity_monitor.py
```

3. Create log directory with appropriate permissions:
```bash
touch /var/log/connectivity.log
chmod 644 /var/log/connectivity.log
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
nano .env
```

## Configuration

1. Open the script and update the following variables:
```python
PUSHOVER_TOKEN = 'YOUR_APP_TOKEN'  # Your Pushover application token
PUSHOVER_USER = 'YOUR_USER_KEY'    # Your Pushover user key
TARGET_URL = 'https://example.com' # URL or IP to monitor
TIMEOUT = 10                       # Request timeout in seconds
MAX_RETRIES = 3                   # Number of retry attempts before reboot
RETRY_DELAY = 30                  # Delay between retries in seconds
```

2. Ensure the script has permissions to execute reboot:
```bash
chmod +s /sbin/reboot  # Only if necessary and security policies allow
```

## Setting up the Cron Job

1. Open the crontab editor:
```bash
crontab -e
```

2. Add the following line to run the script every 5 minutes:
```bash
*/5 * * * * /usr/bin/connectivity_monitor.py
# Add log rotation to run daily at midnight
0 0 * * * /usr/bin/rotate_logs.sh
```

## Testing

Before setting up the cron job, test the configuration:
```bash
python3 test_connectivity.py
```

This will verify:
- Pushover credentials
- Target URL accessibility
- Basic connectivity

## Log File

The script logs all activities to `/var/log/connectivity.log`. The log format includes:
- Timestamp
- Log level (INFO, ERROR)
- Detailed message

Example log entries:
```
2024-03-14 10:30:15 - INFO - Starting connectivity check
2024-03-14 10:30:16 - INFO - Successfully connected to https://example.com
2024-03-14 10:30:17 - ERROR - Connectivity check failed: Connection timeout
2024-03-14 10:30:18 - INFO - Attempting retry 1 of 3
```

## Troubleshooting

1. If the script fails to send notifications:
   - Verify your Pushover credentials
   - Check internet connectivity
   - Review the log file for error messages

2. If the script fails to reboot:
   - Verify sudo permissions
   - Check the system logs
   - Ensure the script has execute permissions

3. If logs aren't being written:
   - Check file permissions on the log file
   - Verify the user running the script has write access

## Security Considerations

1. Store the script in a secure location with restricted access
2. Protect your Pushover credentials
3. Limit sudo privileges to only the necessary command
4. Consider implementing rate limiting for notifications
5. Use HTTPS for the target URL when possible
6. Consider storing sensitive credentials in environment variables

## Customization

You can modify the script to:
- Adjust retry attempts and delays
- Implement different notification services
- Add additional monitoring metrics
- Customize logging format and locations
- Adjust timeout values

## Error Codes

The script uses the following exit codes:
- 0: Success
- 1: General error
- 2: Configuration error
- 3: Network error
- 4: Permission error

## License

This project is licensed under the MIT License - see the LICENSE file for details.
