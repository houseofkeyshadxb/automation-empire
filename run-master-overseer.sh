#!/bin/bash
# Master overseer with process guard

SCRIPT_NAME="master-overseer.py"
LOG_FILE="$HOME/logs/monitoring/overseer-$(date +%Y%m%d).log"

# Check if already running
if pgrep -f "$SCRIPT_NAME" > /dev/null; then
    echo "$(date): Master overseer already running, skipping..." >> "$LOG_FILE"
    exit 0
fi

# Activate venv and run
cd "$HOME" || exit 1
source "$HOME/.env"
/home/userkeysha2000/venv-agents/bin/python3 "$SCRIPT_NAME" >> "$LOG_FILE" 2>&1 || {
    echo "FAIL: Master overseer - $(date)" >> "$HOME/logs/FAILURES.log"
    exit 1
}
