#!/usr/bin/env python3
"""
CALL MONITOR - Watches agents and triggers calls when needed

Monitors:
- Agent status files
- Content approval queue
- Revenue milestones
- System health
- Scheduled check-ins

Triggers claude-calls-you.py when conditions are met
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

# Paths
HOME = Path.home()
AGENTS_DIR = HOME / "agents"
CALL_TRIGGERS = AGENTS_DIR / "call-triggers.json"
AGENT_STATUS_DIR = HOME / "agent-status"
CONTENT_QUEUE_DIR = HOME / "content-approval-queue"
REVENUE_LOG = HOME / "logs" / "revenue.json"
CALL_MONITOR_LOG = HOME / "logs" / "call-monitor.log"
CALL_SCRIPT = HOME / "claude-calls-you.py"

# State tracking
LAST_CALL_TIME = None
CALL_COUNT_HOUR = 0
CALL_COUNT_DAY = 0
HOUR_START = datetime.now()
DAY_START = datetime.now()
NOTIFIED_MILESTONES = set()

def load_triggers():
    """Load call trigger configuration"""
    if not CALL_TRIGGERS.exists():
        print(f"❌ Triggers config not found: {CALL_TRIGGERS}")
        return None

    with open(CALL_TRIGGERS) as f:
        return json.load(f)

def log_event(message):
    """Log monitoring events"""
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}\n"

    print(log_line.strip())

    CALL_MONITOR_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(CALL_MONITOR_LOG, 'a') as f:
        f.write(log_line)

def can_make_call(config):
    """Check if we can make a call (rate limiting)"""
    global LAST_CALL_TIME, CALL_COUNT_HOUR, CALL_COUNT_DAY, HOUR_START, DAY_START

    now = datetime.now()

    # Reset hourly counter
    if (now - HOUR_START).total_seconds() >= 3600:
        CALL_COUNT_HOUR = 0
        HOUR_START = now

    # Reset daily counter
    if (now - DAY_START).total_seconds() >= 86400:
        CALL_COUNT_DAY = 0
        DAY_START = now
        NOTIFIED_MILESTONES.clear()

    rate_limit = config.get("rate_limiting", {})
    max_hour = rate_limit.get("max_calls_per_hour", 10)
    max_day = rate_limit.get("max_calls_per_day", 50)
    cooldown = rate_limit.get("cooldown_between_calls_seconds", 300)

    # Check rate limits
    if CALL_COUNT_HOUR >= max_hour:
        log_event(f"⚠️ Hourly call limit reached ({max_hour})")
        return False

    if CALL_COUNT_DAY >= max_day:
        log_event(f"⚠️ Daily call limit reached ({max_day})")
        return False

    # Check cooldown
    if LAST_CALL_TIME:
        elapsed = (now - LAST_CALL_TIME).total_seconds()
        if elapsed < cooldown:
            log_event(f"⏳ Cooldown active ({int(cooldown - elapsed)}s remaining)")
            return False

    return True

def make_call(message, urgency="medium"):
    """Trigger a call to the user"""
    global LAST_CALL_TIME, CALL_COUNT_HOUR, CALL_COUNT_DAY

    try:
        log_event(f"📞 Making call: {message[:100]}")

        # Choose call method based on urgency
        if urgency == "urgent":
            cmd = [str(CALL_SCRIPT), "--emergency", message]
        else:
            cmd = [str(CALL_SCRIPT), message]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            LAST_CALL_TIME = datetime.now()
            CALL_COUNT_HOUR += 1
            CALL_COUNT_DAY += 1
            log_event(f"✅ Call successful (Hour: {CALL_COUNT_HOUR}, Day: {CALL_COUNT_DAY})")
            return True
        else:
            log_event(f"❌ Call failed: {result.stderr}")
            return False

    except Exception as e:
        log_event(f"❌ Call error: {e}")
        return False

def check_agent_stuck(config):
    """Check if any agent is stuck"""
    trigger = config["triggers"].get("agent_stuck", {})
    if not trigger.get("enabled", False):
        return

    if not AGENT_STATUS_DIR.exists():
        return

    for status_file in AGENT_STATUS_DIR.glob("*.json"):
        try:
            with open(status_file) as f:
                status = json.load(f)

            agent_name = status.get("name", status_file.stem)
            state = status.get("status", "")
            started = status.get("started_at", "")

            if state == "running" and started:
                start_time = datetime.fromisoformat(started)
                duration = (datetime.now() - start_time).total_seconds() / 60

                # Stuck if running > 10 minutes without progress
                if duration > 10:
                    last_update = status.get("last_update", "")
                    if last_update:
                        update_time = datetime.fromisoformat(last_update)
                        idle = (datetime.now() - update_time).total_seconds() / 60
                        if idle > 10:
                            message = trigger["message_template"].format(
                                agent_name=agent_name,
                                task=status.get("current_task", "unknown task"),
                                duration=int(duration)
                            )
                            if can_make_call(config):
                                make_call(message, "medium")
                                # Mark as notified
                                status["notified_stuck"] = datetime.now().isoformat()
                                with open(status_file, 'w') as f:
                                    json.dump(status, f, indent=2)

        except Exception as e:
            log_event(f"Error checking {status_file}: {e}")

def check_content_queue(config):
    """Check content approval queue size"""
    trigger = config["triggers"].get("content_approval_queue", {})
    if not trigger.get("enabled", False):
        return

    if not CONTENT_QUEUE_DIR.exists():
        return

    # Count items in queue
    queue_items = list(CONTENT_QUEUE_DIR.glob("*.json"))
    count = len(queue_items)

    if count > 50:
        # Estimate revenue
        estimated = count * 10  # $10 per content piece average

        message = trigger["message_template"].format(
            count=count,
            estimated_revenue=estimated
        )

        if can_make_call(config):
            make_call(message, "medium")

def check_revenue_milestone(config):
    """Check if revenue milestone hit"""
    trigger = config["triggers"].get("revenue_milestone", {})
    if not trigger.get("enabled", False):
        return

    if not REVENUE_LOG.exists():
        return

    try:
        with open(REVENUE_LOG) as f:
            revenue_data = json.load(f)

        today = datetime.now().strftime("%Y-%m-%d")
        daily = revenue_data.get("daily", {}).get(today, 0)

        thresholds = trigger.get("thresholds", [100, 500, 1000, 5000, 10000])

        for threshold in thresholds:
            if daily >= threshold and threshold not in NOTIFIED_MILESTONES:
                # Calculate monthly projection
                day_of_month = datetime.now().day
                days_in_month = 30
                monthly_projection = (daily / day_of_month) * days_in_month

                message = trigger["message_template"].format(
                    amount=daily,
                    monthly_projection=int(monthly_projection)
                )

                if can_make_call(config):
                    make_call(message, "low")
                    NOTIFIED_MILESTONES.add(threshold)

    except Exception as e:
        log_event(f"Error checking revenue: {e}")

def check_system_health(config):
    """Check if critical systems are down"""
    trigger = config["triggers"].get("system_down", {})
    if not trigger.get("enabled", False):
        return

    # Check if dashboard is accessible
    dashboard_file = HOME / "dashboard" / "status.json"
    if dashboard_file.exists():
        try:
            with open(dashboard_file) as f:
                status = json.load(f)

            last_update = status.get("last_update", "")
            if last_update:
                update_time = datetime.fromisoformat(last_update)
                idle = (datetime.now() - update_time).total_seconds()

                # If dashboard hasn't updated in 10 minutes, system might be down
                if idle > 600:
                    message = trigger["message_template"].format(
                        component="Dashboard",
                        uptime=f"{int(idle/60)} minutes ago"
                    )
                    if can_make_call(config):
                        make_call(message, "urgent")

        except Exception as e:
            log_event(f"Error checking dashboard: {e}")

def main():
    """Main monitoring loop"""
    log_event("🚀 Call Monitor started")

    config = load_triggers()
    if not config:
        log_event("❌ Failed to load config, exiting")
        sys.exit(1)

    # Make script executable
    if CALL_SCRIPT.exists():
        os.chmod(CALL_SCRIPT, 0o755)

    log_event(f"✅ Loaded {len(config['triggers'])} triggers")
    log_event(f"📞 Call script: {CALL_SCRIPT}")

    # Monitoring loop
    while True:
        try:
            # Check all triggers
            check_agent_stuck(config)
            check_content_queue(config)
            check_revenue_milestone(config)
            check_system_health(config)

            # Sleep for 60 seconds
            time.sleep(60)

        except KeyboardInterrupt:
            log_event("👋 Call Monitor stopped by user")
            break
        except Exception as e:
            log_event(f"❌ Monitor error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
