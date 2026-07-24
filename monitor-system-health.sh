#!/bin/bash
# System health monitor - Detects and kills duplicate processes

LOG_FILE="$HOME/logs/monitoring/health-$(date +%Y%m%d).log"
ALERT_FILE="$HOME/logs/SYSTEM-ALERTS.log"

echo "=== System Health Check - $(date) ===" >> "$LOG_FILE"

# Check memory usage
MEM_USAGE=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')
MEM_THRESHOLD=85

if (( $(echo "$MEM_USAGE > $MEM_THRESHOLD" | bc -l) )); then
    echo "WARNING: Memory usage at ${MEM_USAGE}%" >> "$ALERT_FILE"
    echo "WARNING: High memory usage detected: ${MEM_USAGE}%" >> "$LOG_FILE"
fi

# Check for duplicate processes
DUPLICATES=$(pgrep -c -f "telegram-bot-live.js")
if [ "$DUPLICATES" -gt 1 ]; then
    echo "WARNING: Found $DUPLICATES telegram bot instances. Killing all..." >> "$ALERT_FILE"
    pkill -f telegram-bot-live.js
    echo "Killed duplicate telegram bots" >> "$LOG_FILE"
fi

DUPLICATES=$(pgrep -c -f "master-overseer.py")
if [ "$DUPLICATES" -gt 1 ]; then
    echo "WARNING: Found $DUPLICATES master overseer instances. Killing all..." >> "$ALERT_FILE"
    pkill -f master-overseer.py
    echo "Killed duplicate master overseers" >> "$LOG_FILE"
fi

# Check disk space
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
DISK_THRESHOLD=90

if [ "$DISK_USAGE" -gt "$DISK_THRESHOLD" ]; then
    echo "WARNING: Disk usage at ${DISK_USAGE}%" >> "$ALERT_FILE"
    echo "WARNING: High disk usage detected: ${DISK_USAGE}%" >> "$LOG_FILE"

    # Auto-cleanup old logs
    find "$HOME/logs" -name "*.log" -mtime +14 -exec gzip {} \;
    echo "Compressed logs older than 14 days" >> "$LOG_FILE"
fi

# Count active Python/Node processes
PROCESS_COUNT=$(ps aux | grep -E '(python|node)' | grep -v grep | wc -l)
echo "Active Python/Node processes: $PROCESS_COUNT" >> "$LOG_FILE"

if [ "$PROCESS_COUNT" -gt 20 ]; then
    echo "WARNING: Too many processes running: $PROCESS_COUNT" >> "$ALERT_FILE"
    ps aux | grep -E '(python|node)' | grep -v grep >> "$LOG_FILE"
fi

# Report status
echo "Memory: ${MEM_USAGE}% | Disk: ${DISK_USAGE}% | Processes: $PROCESS_COUNT" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
