#!/bin/bash
# Inbox guardian with process guard

SCRIPT_NAME="inbox-guardian.py"
LOG_FILE="$HOME/logs/agents/inbox-$(date +%Y%m%d).log"

# Check if already running
if pgrep -f "$SCRIPT_NAME" > /dev/null; then
    echo "$(date): Inbox guardian already running, skipping..." >> "$LOG_FILE"
    exit 0
fi

# Activate venv and run
cd "$HOME/agents" || exit 1
source "$HOME/.env"
/home/userkeysha2000/venv-agents/bin/python3 "$SCRIPT_NAME" >> "$LOG_FILE" 2>&1 || {
    echo "FAIL: Inbox guardian - $(date)" >> "$HOME/logs/FAILURES.log"
    exit 1
}
