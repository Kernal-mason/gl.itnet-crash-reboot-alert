# Connectivity Monitor

Author: Mason Gonzalez
Created: March 2024
License: MIT
Repository: https://github.com/Kernal-mason/gl.itnet-crash-reboot-alert

A Python script that monitors network connectivity and automatically reboots the system if connectivity fails, with Pushover notifications for alerts.

## Features

- Continuous monitoring of specified URL/IP
- Notifications via Pushover or Telegram for connectivity failures and system events
- Automatic system reboot on connectivity failure
- Comprehensive logging to both file and stdout
- Error handling and timeout management

## Prerequisites

- Python 3.6 or higher
- GL-iNet router or other Busybox-based system
- Pushover account or Telegram account (for notifications)

### GL-iNet Router Specific

Most GL-iNet routers come with Python3 and BusyBox pre-installed. You may need to:

1. Enable external storage if installing on a router with limited space:
```bash
opkg update
opkg install kmod-usb-storage
```

2. Install pip if not already available:
```bash
opkg install python3-pip
```

## Installation

There are two ways to install the Connectivity Monitor:

### Automatic Installation

1. Clone the repository:
```bash
git clone https://github.com/Kernal-mason/gl.itnet-crash-reboot-alert.git
cd gl.itnet-crash-reboot-alert
```

2. Configure your environment:
```bash
cp .env.example .env
vi .env  # Edit with your Pushover credentials and settings
```

3. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

4. Verify the installation:
```bash
python3 test_connectivity.py
```

### Manual Installation

1. Install required Python packages:
```bash
opkg update  # or your system's package manager
opkg install python3-pip
pip3 install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
nano .env  # Edit with your Pushover credentials and settings
```

3. Clone or copy the script:
```bash
cp connectivity_monitor.py /usr/bin/
chmod +x /usr/bin/connectivity_monitor.py
cp rotate_logs.sh /usr/bin/
chmod +x /usr/bin/rotate_logs.sh
```

4. Create log directory with appropriate permissions:
```bash
touch /var/log/connectivity.log
chmod 644 /var/log/connectivity.log
```

### Post-Installation

After either installation method:

1. Verify the configuration:
```bash
python3 test_connectivity.py
```

2. If the test fails:
   - Check your Pushover credentials in .env
   - Verify network connectivity
   - Review permissions

3. The cron jobs should be automatically configured. Verify them with:
```bash
cat /etc/crontabs/root
```

## Configuration

The following environment variables can be configured in your `.env` file:

### Notification Type
```python
# Choose your preferred notification service
NOTIFICATION_TYPE=pushover  # or 'telegram'
```

### Pushover Configuration
```python
# Only needed if using Pushover
PUSHOVER_TOKEN=your_pushover_token_here  # Your Pushover application token
PUSHOVER_USER=your_pushover_user_here    # Your Pushover user key
```

To set up Pushover:
1. Create an account at https://pushover.net
2. Create a new application to get your API token
3. Get your user key from your account dashboard

### Telegram Configuration
```python
# Only needed if using Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here  # Your Telegram bot token
TELEGRAM_CHAT_ID=your_chat_id_here      # Your Telegram chat ID
```

To set up Telegram:
1. Create a new bot using @BotFather on Telegram
2. Get your bot token from BotFather
3. Send a message to your bot
4. Get your chat ID by visiting:
   https://api.telegram.org/bot<YourBOTToken>/getUpdates

### General Configuration
```python
TARGET_URL=https://example.com           # URL or IP to monitor
TIMEOUT=5                                # Request timeout in seconds
MAX_RETRIES=3                           # Number of retry attempts
RETRY_DELAY=15                          # Delay between retries in seconds
LOG_PATH=/var/log/connectivity.log      # Path to log file
```

2. Ensure the script has permissions to execute reboot:
```bash
chmod +s /sbin/reboot  # Only if necessary and security policies allow
```

## Setting up the Cron Job

### GL-iNet/BusyBox Systems

The installation script automatically sets up the cron jobs in `/etc/crontabs/root`. 
To manually configure:

1. Open the crontab file:
```bash
vi /etc/crontabs/root
```

2. Add the following line to run the script every 5 minutes:
```bash
*/5 * * * * /usr/bin/connectivity_monitor.py
# Add log rotation to run daily at midnight
0 0 * * * /usr/bin/rotate_logs.sh
```

3. Restart the cron daemon:
```bash
/etc/init.d/cron restart
```

## Testing

There are several ways to test the connectivity monitor:

### 1. Using the Test Script
```bash
python3 test_connectivity.py
```

This automated test will verify:
- Pushover credentials
- Target URL accessibility
- Basic connectivity

### 2. Manual Testing

1. Test notification service:
```bash
# For Pushover
curl -X POST "https://api.pushover.net/1/messages.json" \
  --form-string "token=$PUSHOVER_TOKEN" \
  --form-string "user=$PUSHOVER_USER" \
  --form-string "message=Test notification"

# For Telegram
curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -d "chat_id=$TELEGRAM_CHAT_ID" \
  -d "text=Test notification"
```

2. Test environment configuration:
```bash
cat /usr/bin/.env  # Verify environment variables are set correctly
```

3. Test Pushover notifications:
```bash
# Run the script directly to test connectivity and notifications
python3 /usr/bin/connectivity_monitor.py
```

4. Test log rotation:
```bash
# Create a large log file
yes "test log entry" | head -n 1000 >> /var/log/connectivity.log

# Run log rotation
/usr/bin/rotate_logs.sh

# Verify rotation worked
ls -l /var/log/connectivity*
```

5. Test cron configuration:
```bash
# Check cron job setup
cat /etc/crontabs/root

# Verify cron daemon is running
/etc/init.d/cron status
```

### 3. Simulating Failures

1. Network failure test:
```bash
# Temporarily change TARGET_URL to an invalid address
sed -i 's/TARGET_URL=.*/TARGET_URL=https:\/\/invalid.example.com/' /usr/bin/.env

# Run the script
python3 /usr/bin/connectivity_monitor.py

# Check the logs
tail -f /var/log/connectivity.log

# Don't forget to change TARGET_URL back!
```

2. Permission test:
```bash
# Verify reboot permission
ls -l /sbin/reboot
```

### 4. Monitoring

Monitor the script's operation:
```bash
# Watch the log file in real-time
tail -f /var/log/connectivity.log

# Check Pushover notification history in your Pushover app
```

### Common Test Issues

1. If test_connectivity.py fails:
   - Verify network connectivity
   - Check Pushover credentials
   - Ensure TARGET_URL is accessible

2. If notifications aren't received:
   - Verify Pushover tokens in .env
   - Check internet connectivity
   - Look for errors in the log file

3. If cron jobs aren't running:
   - Check cron daemon status
   - Verify file permissions
   - Check system time is correct

### Production Deployment

Before deploying to production:
1. Run all tests successfully
2. Verify log rotation is working
3. Test actual reboot functionality
4. Monitor for false positives
5. Adjust timeouts and retries as needed

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

### GL-iNet Specific Issues

1. If Python packages fail to install:
   - Ensure you have enough storage space
   - Try installing to external storage if available

2. If cron jobs don't run:
   - Check if cron daemon is running: `/etc/init.d/cron status`
   - Verify cron file permissions: `chmod 600 /etc/crontabs/root`
   - Restart cron daemon: `/etc/init.d/cron restart`

3. If storage space is limited:
   - Consider mounting external storage
   - Adjust log rotation size in rotate_logs.sh
   - Monitor space usage with `df -h`

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
