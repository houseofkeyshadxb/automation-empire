#!/usr/bin/env python3
"""
COMMAND EXECUTOR AGENT
Automatically runs terminal commands so nothing is left pending
No more "you need to run this command" - this agent DOES IT!
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

class CommandExecutor:
    def __init__(self):
        self.log_file = Path.home() / "logs" / "command-executor.log"
        self.log_file.parent.mkdir(exist_ok=True)
        self.pending_commands = []

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        print(log_entry.strip())
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

    def execute(self, command, description="", timeout=300):
        """Execute a shell command and return result"""
        self.log(f"🚀 EXECUTING: {description or command}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(Path.home())
            )

            if result.returncode == 0:
                self.log(f"✅ SUCCESS: {description or command}")
                if result.stdout:
                    self.log(f"Output: {result.stdout[:500]}")
                return True, result.stdout
            else:
                self.log(f"❌ FAILED: {description or command}")
                self.log(f"Error: {result.stderr}")
                return False, result.stderr

        except subprocess.TimeoutExpired:
            self.log(f"⏱️ TIMEOUT: {description or command}")
            return False, "Command timed out"
        except Exception as e:
            self.log(f"💥 EXCEPTION: {str(e)}")
            return False, str(e)

    def execute_queue(self, commands):
        """Execute a queue of commands in order"""
        results = []

        for cmd in commands:
            command = cmd.get('command')
            description = cmd.get('description', '')
            critical = cmd.get('critical', False)

            success, output = self.execute(command, description)

            results.append({
                'command': command,
                'description': description,
                'success': success,
                'output': output
            })

            # If critical command fails, stop execution
            if critical and not success:
                self.log(f"🛑 CRITICAL COMMAND FAILED - STOPPING QUEUE")
                break

        return results

# PENDING COMMANDS QUEUE
PENDING_COMMANDS = [
    {
        'command': 'pip install --break-system-packages selenium webdriver-manager requests',
        'description': 'Install account creation bot dependencies',
        'critical': True
    },
    {
        'command': 'cd ~/agents/inbox-guardian && chmod +x deploy.sh',
        'description': 'Make Helena deploy script executable',
        'critical': False
    },
    {
        'command': 'cd ~/agents/content-engine && chmod +x run.sh',
        'description': 'Make Marcus run script executable',
        'critical': False
    },
    {
        'command': 'cd ~/revenue-systems && chmod +x setup.sh',
        'description': 'Make revenue system setup executable',
        'critical': False
    },
    {
        'command': 'chmod +x ~/CREATE-ALL-ACCOUNTS-TODAY.sh',
        'description': 'Make account creation script executable',
        'critical': True
    },
    {
        'command': 'chmod +x ~/account-creation-bot.py',
        'description': 'Make account bot executable',
        'critical': True
    },
]

def main():
    print("🤖 COMMAND EXECUTOR AGENT - AUTO-RUNNING ALL PENDING COMMANDS")
    print("="*60)
    print("")

    executor = CommandExecutor()

    # Execute all pending commands
    results = executor.execute_queue(PENDING_COMMANDS)

    # Summary
    print("\n" + "="*60)
    print("📊 EXECUTION SUMMARY")
    print("="*60)

    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)

    print(f"\n✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")

    print("\n📋 DETAILED RESULTS:")
    for i, result in enumerate(results, 1):
        status = "✅" if result['success'] else "❌"
        print(f"\n{i}. {status} {result['description']}")
        if not result['success']:
            print(f"   Error: {result['output'][:200]}")

    print(f"\n📝 Full log: {executor.log_file}")

    # Save results
    results_file = Path.home() / "logs" / "command-execution-results.json"
    with open(results_file, 'w') as f:
        json.dump({
            'executed_at': datetime.now().isoformat(),
            'total': total_count,
            'successful': success_count,
            'failed': total_count - success_count,
            'results': results
        }, f, indent=2)

    print(f"💾 Results saved: {results_file}")

if __name__ == '__main__':
    main()
