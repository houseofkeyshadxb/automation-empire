#!/bin/bash
# Telegram bot with process guard

SCRIPT_NAME="telegram-bot-live.js"
LOG_FILE="$HOME/logs/telegram/bot-$(date +%Y%m%d).log"

# Check if already running
if pgrep -f "$SCRIPT_NAME" > /dev/null; then
    echo "$(date): Telegram bot already running, skipping..." >> "$LOG_FILE"
    exit 0
fi

# Run the bot
cd "$HOME" || exit 1
node "$SCRIPT_NAME" >> "$LOG_FILE" 2>&1 || {
    echo "FAIL: Telegram bot - $(date)" >> "$HOME/logs/FAILURES.log"
    exit 1
}
