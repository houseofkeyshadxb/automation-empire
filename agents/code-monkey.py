#!/usr/bin/env python3
"""
Code Monkey AI Agent - On-demand script generation and automation
From AI Agent Empire PDF

WHAT IT DOES:
- Listens for commands via Telegram bot
- Generates Python/Bash scripts on demand
- Saves scripts with timestamps
- Executes simple scripts and returns results
- Logs all requests to Supabase

COMMANDS:
/script [description] - Generate a new script
/doc [file_path] - Generate documentation for a file
/execute [script_name] - Run a saved script and return output
/list - Show all generated scripts
/help - Show command list
"""

import os
import sys
import logging
import json
import subprocess
from datetime import datetime
from pathlib import Path
import requests
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser('~/.env'))

# Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8656145107:AAHsxcAWn-Fua-mRpEC3xn3xjKTW_YvVTE0")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-key-here")
SCRIPTS_DIR = Path.home() / "generated-scripts"
LOGS_DIR = Path.home() / "logs"
BOT_USERNAME = "@MistressKeyshaDXBPrivate_bot"

# Ensure directories exist
SCRIPTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "code-monkey.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CodeMonkey")

# Telegram API base URL
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None


def send_telegram_message(chat_id, text, parse_mode="Markdown"):
    """Send a message via Telegram bot"""
    try:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        response = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("ok", False)
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


def send_document(chat_id, file_path, caption=""):
    """Send a file via Telegram bot"""
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': chat_id, 'caption': caption}
            response = requests.post(f"{TELEGRAM_API}/sendDocument", files=files, data=data, timeout=30)
            response.raise_for_status()
            return response.json().get("ok", False)
    except Exception as e:
        logger.error(f"Failed to send document: {e}")
        return False


def log_to_supabase(request_type, description, script_path=None, status="completed"):
    """Log request to Supabase code_requests table"""
    try:
        if SUPABASE_URL == "https://your-project.supabase.co":
            logger.warning("Supabase not configured, skipping logging")
            return

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "request_type": request_type,
            "description": description,
            "script_path": str(script_path) if script_path else None,
            "status": status,
            "created_at": datetime.utcnow().isoformat()
        }

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/code_requests",
            headers=headers,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        logger.info(f"Logged to Supabase: {request_type}")
    except Exception as e:
        logger.error(f"Failed to log to Supabase: {e}")


def generate_script_with_claude(description, language="python"):
    """Generate a script using Claude AI"""
    if not client:
        return None, "Claude API key not configured"

    try:
        prompt = f"""Generate a complete, production-ready {language} script based on this description:

{description}

Requirements:
- Include all necessary imports
- Add proper error handling
- Include helpful comments
- Make it executable and ready to run
- Add usage instructions in the docstring
- Follow best practices

Return ONLY the script code, no explanations."""

        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        script_content = message.content[0].text

        # Clean up markdown code blocks if present
        if script_content.startswith("```"):
            lines = script_content.split("\n")
            script_content = "\n".join(lines[1:-1])

        return script_content, None
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return None, str(e)


def generate_documentation(file_path):
    """Generate documentation for a file using Claude AI"""
    if not client:
        return None, "Claude API key not configured"

    try:
        if not os.path.exists(file_path):
            return None, f"File not found: {file_path}"

        with open(file_path, 'r') as f:
            code_content = f.read()

        prompt = f"""Generate comprehensive documentation for this code file:

File: {file_path}

```
{code_content}
```

Include:
- Overview/Purpose
- Key functions/classes
- Usage examples
- Dependencies
- Configuration needed

Format as clean Markdown."""

        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text, None
    except Exception as e:
        logger.error(f"Documentation generation error: {e}")
        return None, str(e)


def save_script(content, description, language="python"):
    """Save generated script with timestamp"""
    # Create safe filename
    safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '-' for c in description.lower())
    safe_name = safe_name[:50]  # Limit length
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    ext = "py" if language == "python" else "sh"
    filename = f"{safe_name}-{timestamp}.{ext}"
    filepath = SCRIPTS_DIR / filename

    # Write script
    with open(filepath, 'w') as f:
        f.write(content)

    # Make executable
    os.chmod(filepath, 0o755)

    logger.info(f"Script saved: {filepath}")
    return filepath


def execute_script(script_name, chat_id):
    """Execute a saved script and return output"""
    script_path = SCRIPTS_DIR / script_name

    if not script_path.exists():
        return None, f"Script not found: {script_name}"

    try:
        # Send initial message
        send_telegram_message(chat_id, f"⚙️ Executing `{script_name}`...\nThis may take a moment...")

        # Execute with timeout
        result = subprocess.run(
            [str(script_path)],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout
            cwd=str(SCRIPTS_DIR)
        )

        output = f"**Exit Code:** {result.returncode}\n\n"

        if result.stdout:
            output += f"**STDOUT:**\n```\n{result.stdout[:1000]}\n```\n\n"

        if result.stderr:
            output += f"**STDERR:**\n```\n{result.stderr[:1000]}\n```"

        return output, None
    except subprocess.TimeoutExpired:
        return None, "Script execution timed out (60s limit)"
    except Exception as e:
        return None, f"Execution error: {str(e)}"


def list_scripts():
    """List all generated scripts"""
    scripts = list(SCRIPTS_DIR.glob("*.py")) + list(SCRIPTS_DIR.glob("*.sh"))
    scripts.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    if not scripts:
        return "📂 No scripts generated yet.\n\nUse `/script [description]` to create one!"

    output = "📂 **Generated Scripts:**\n\n"
    for i, script in enumerate(scripts[:20], 1):  # Show latest 20
        size = script.stat().st_size
        modified = datetime.fromtimestamp(script.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        output += f"{i}. `{script.name}`\n   Size: {size} bytes | Modified: {modified}\n\n"

    if len(scripts) > 20:
        output += f"\n...and {len(scripts) - 20} more scripts"

    return output


def handle_command(chat_id, command, args):
    """Handle incoming Telegram commands"""
    logger.info(f"Command: {command} | Args: {args}")

    if command == "/start" or command == "/help":
        help_text = """🐒 **Code Monkey AI Agent**

I generate scripts and documentation on-demand!

**Commands:**

`/script [description]` - Generate a new script
Example: `/script download all my Instagram stories`

`/doc [file_path]` - Generate documentation
Example: `/doc ~/agents/code-monkey.py`

`/execute [script_name]` - Run a saved script
Example: `/execute download-instagram-2026-06-20.py`

`/list` - Show all generated scripts

`/help` - Show this message

**Status:** ✅ Online and ready to code!"""
        send_telegram_message(chat_id, help_text)
        return

    if command == "/list":
        scripts_list = list_scripts()
        send_telegram_message(chat_id, scripts_list)
        return

    if command == "/script":
        if not args:
            send_telegram_message(chat_id, "❌ Please provide a script description.\n\nExample: `/script download Instagram stories`")
            return

        send_telegram_message(chat_id, f"🐒 Generating script: *{args}*\n\nPlease wait...")

        # Generate script
        script_content, error = generate_script_with_claude(args)

        if error:
            send_telegram_message(chat_id, f"❌ Error: {error}")
            log_to_supabase("script", args, status="failed")
            return

        # Save script
        script_path = save_script(script_content, args)

        # Log to Supabase
        log_to_supabase("script", args, script_path, "completed")

        # Send success message with script
        success_msg = f"✅ **Script Generated!**\n\n📁 Saved to: `{script_path.name}`\n\n🧪 Testing now..."
        send_telegram_message(chat_id, success_msg)

        # Send the script file
        send_document(chat_id, script_path, caption=f"Generated script: {args}")

        # Try to execute for simple validation
        output, exec_error = execute_script(script_path.name, chat_id)

        if exec_error:
            send_telegram_message(chat_id, f"⚠️ Script saved but test execution failed:\n`{exec_error}`\n\nYou may need to customize it for your environment.")
        else:
            send_telegram_message(chat_id, f"✅ **Script works!**\n\n{output[:1000]}")

        return

    if command == "/doc":
        if not args:
            send_telegram_message(chat_id, "❌ Please provide a file path.\n\nExample: `/doc ~/agents/code-monkey.py`")
            return

        send_telegram_message(chat_id, f"📝 Generating documentation for: *{args}*\n\nPlease wait...")

        # Expand ~ to home directory
        file_path = os.path.expanduser(args)

        # Generate documentation
        doc_content, error = generate_documentation(file_path)

        if error:
            send_telegram_message(chat_id, f"❌ Error: {error}")
            log_to_supabase("documentation", args, status="failed")
            return

        # Save documentation
        doc_filename = f"{Path(file_path).stem}-docs-{datetime.now().strftime('%Y-%m-%d')}.md"
        doc_path = SCRIPTS_DIR / doc_filename

        with open(doc_path, 'w') as f:
            f.write(doc_content)

        # Log to Supabase
        log_to_supabase("documentation", args, doc_path, "completed")

        # Send documentation
        send_telegram_message(chat_id, f"✅ **Documentation Generated!**\n\n📁 Saved to: `{doc_filename}`")
        send_document(chat_id, doc_path, caption=f"Documentation for: {args}")

        return

    if command == "/execute":
        if not args:
            send_telegram_message(chat_id, "❌ Please provide a script name.\n\nUse `/list` to see available scripts.")
            return

        output, error = execute_script(args, chat_id)

        if error:
            send_telegram_message(chat_id, f"❌ Execution failed:\n`{error}`")
            log_to_supabase("execute", args, status="failed")
        else:
            send_telegram_message(chat_id, f"✅ **Execution Complete!**\n\n{output}")
            log_to_supabase("execute", args, status="completed")

        return

    # Unknown command
    send_telegram_message(chat_id, f"❓ Unknown command: `{command}`\n\nUse `/help` to see available commands.")


def process_updates(updates):
    """Process incoming Telegram updates"""
    for update in updates:
        try:
            if "message" not in update:
                continue

            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if not text.startswith("/"):
                continue

            # Parse command and args
            parts = text.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # Handle command
            handle_command(chat_id, command, args)

        except Exception as e:
            logger.error(f"Error processing update: {e}")


def main():
    """Main bot loop"""
    logger.info("🐒 Code Monkey AI Agent starting...")
    logger.info(f"Scripts directory: {SCRIPTS_DIR}")
    logger.info(f"Logs directory: {LOGS_DIR}")
    logger.info(f"Bot username: {BOT_USERNAME}")

    if not client:
        logger.warning("⚠️ Anthropic API key not set - script generation disabled")
        logger.warning("Set ANTHROPIC_API_KEY environment variable")

    offset = 0

    while True:
        try:
            # Get updates
            params = {"offset": offset, "timeout": 30}
            response = requests.get(f"{TELEGRAM_API}/getUpdates", params=params, timeout=35)
            response.raise_for_status()

            data = response.json()

            if not data.get("ok"):
                logger.error(f"Telegram API error: {data.get('description')}")
                continue

            updates = data.get("result", [])

            if updates:
                # Process updates
                process_updates(updates)

                # Update offset
                offset = updates[-1]["update_id"] + 1

        except KeyboardInterrupt:
            logger.info("Shutting down Code Monkey...")
            break

        except Exception as e:
            logger.error(f"Main loop error: {e}")
            import time
            time.sleep(5)


if __name__ == "__main__":
    main()
