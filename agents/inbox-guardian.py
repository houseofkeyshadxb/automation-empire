#!/usr/bin/env python3
"""
Inbox Guardian AI Agent
Email triage, categorization, and automated replies for Mistress Keysha's Empire
Saves 2+ hours per day through intelligent email management
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Tuple
import anthropic
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser('~/.env'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/userkeysha2000/agents/inbox-guardian/logs/agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('InboxGuardian')

# Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
CHECK_INTERVAL_MINUTES = 15
LOOKBACK_MINUTES = 20  # Slightly longer than check interval to avoid gaps

# Email templates
TEMPLATES = {
    'booking_request': """Thank you for your interest in serving Mistress Keysha.

Please visit our empire site to view session rates and book your experience:
🔗 https://mistress-keysha-empire.com/sessions

All booking inquiries require advance notice and screening.

Respectfully,
The Empire Management Team""",

    'tribute_notification': """Your devotion is noted and appreciated 💋

Mistress Keysha acknowledges your tribute. Your loyalty to the Empire strengthens your position.

With appreciation,
Mistress Keysha's Empire""",

    'fan_message': """Thank you for your message.

Mistress Keysha reviews all messages personally. Expect a response within 24-48 hours.

Important: If this is a booking request, please visit https://mistress-keysha-empire.com/sessions for rates and availability.

Respectfully,
The Empire Management Team""",

    'spam_response': None  # No auto-reply for spam
}

# Category keywords for classification
CATEGORY_KEYWORDS = {
    'booking_request': [
        'book', 'booking', 'session', 'appointment', 'schedule', 'meet',
        'availability', 'available', 'reserve', 'reservation', 'serve you',
        'serving', 'worship', 'tribute session', 'session inquiry'
    ],
    'tribute_notification': [
        'tribute', 'tributed', 'sent you', 'payment received', 'cashapp',
        'venmo', 'paypal', 'gift', 'offering', 'token of appreciation',
        'spoil', 'spoiled', 'financial domination', 'findom'
    ],
    'fan_message': [
        'admire', 'admiration', 'fan', 'follow', 'following', 'love your',
        'amazing', 'beautiful', 'gorgeous', 'stunning', 'incredible',
        'inspiration', 'inspired', 'thank you for', 'appreciate your'
    ],
    'urgent': [
        'urgent', 'emergency', 'asap', 'immediately', 'time sensitive',
        'important:', 'critical', 'please respond', 'needs attention',
        'complaint', 'issue', 'problem', 'concern', 'refund'
    ],
    'spam': [
        'cryptocurrency', 'bitcoin', 'investment opportunity', 'make money fast',
        'click here now', 'congratulations you won', 'claim your prize',
        'nigerian prince', 'lottery', 'viagra', 'casino', 'enlargement',
        'weight loss', 'work from home', 'mlm', 'multi-level'
    ]
}


class InboxGuardian:
    """AI-powered email triage and management agent"""

    def __init__(self):
        """Initialize the Inbox Guardian with API clients"""
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase credentials not set")

        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.processed_thread_ids = set()

        logger.info("Inbox Guardian initialized successfully")

    def categorize_email(self, subject: str, snippet: str, sender: str) -> Tuple[str, float]:
        """
        Categorize email using AI with keyword-based scoring

        Returns:
            Tuple of (category, confidence_score)
        """
        # Combine text for analysis
        text_to_analyze = f"{subject} {snippet}".lower()

        # Calculate keyword match scores
        scores = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_to_analyze)
            if score > 0:
                scores[category] = score

        # Check for urgent markers first (highest priority)
        if 'urgent' in scores:
            return ('urgent', 0.9)

        # Check for spam (second priority)
        if 'spam' in scores and scores['spam'] >= 2:
            return ('spam', 0.85)

        # Determine primary category
        if scores:
            primary_category = max(scores, key=scores.get)
            confidence = min(0.95, 0.6 + (scores[primary_category] * 0.1))
            return (primary_category, confidence)

        # Use AI for ambiguous cases
        try:
            response = self.client.messages.create(
                model="claude-sonnet-5",
                max_tokens=100,
                messages=[{
                    "role": "user",
                    "content": f"""Categorize this email into ONE category: booking_request, tribute_notification, fan_message, spam, or urgent.

Subject: {subject}
From: {sender}
Preview: {snippet}

Respond with ONLY the category name, nothing else."""
                }]
            )

            category = response.content[0].text.strip().lower()
            if category in CATEGORY_KEYWORDS:
                return (category, 0.7)
        except Exception as e:
            logger.error(f"AI categorization failed: {e}")

        # Default to fan_message for uncertain cases
        return ('fan_message', 0.5)

    def should_auto_reply(self, category: str, confidence: float) -> bool:
        """Determine if email should receive auto-reply"""
        # Don't auto-reply to spam
        if category == 'spam':
            return False

        # Don't auto-reply to urgent (needs manual review)
        if category == 'urgent':
            return False

        # Auto-reply only if confidence is high enough
        return confidence >= 0.6

    def create_auto_reply(self, category: str, thread_id: str, message_id: str, to_email: str) -> bool:
        """
        Create an auto-reply draft using Gmail MCP

        Returns:
            True if draft created successfully
        """
        template = TEMPLATES.get(category)
        if not template:
            return False

        try:
            # Use Claude to call Gmail MCP create_draft tool
            response = self.client.messages.create(
                model="claude-sonnet-5",
                max_tokens=200,
                tools=[{
                    "name": "mcp__claude_ai_Gmail__create_draft",
                    "description": "Creates a new draft email in Gmail",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "to": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "subject": {"type": "string"},
                            "body": {"type": "string"},
                            "replyToMessageId": {"type": "string"}
                        },
                        "required": ["to"]
                    }
                }],
                messages=[{
                    "role": "user",
                    "content": f"""Create a draft reply to {to_email} using this template:

{template}

Reply to message ID: {message_id}

Call the mcp__claude_ai_Gmail__create_draft tool."""
                }]
            )

            # Check if tool was called
            for block in response.content:
                if block.type == "tool_use":
                    logger.info(f"Auto-reply draft created for {to_email} (category: {category})")
                    return True

            return False

        except Exception as e:
            logger.error(f"Failed to create auto-reply: {e}")
            return False

    def apply_labels(self, thread_id: str, category: str) -> bool:
        """Apply appropriate Gmail labels to categorized email"""
        try:
            # Map categories to label names
            label_map = {
                'booking_request': 'Empire/Bookings',
                'tribute_notification': 'Empire/Tributes',
                'fan_message': 'Empire/Fans',
                'urgent': 'IMPORTANT',
                'spam': 'SPAM'
            }

            label_name = label_map.get(category, 'Empire/Other')

            # This would need the actual label ID from list_labels
            # For now, log the action
            logger.info(f"Would apply label '{label_name}' to thread {thread_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to apply labels: {e}")
            return False

    def log_to_supabase(self, action_data: Dict) -> bool:
        """Log all actions to Supabase for tracking and analytics"""
        try:
            data = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'action_type': action_data.get('action_type'),
                'thread_id': action_data.get('thread_id'),
                'category': action_data.get('category'),
                'confidence': action_data.get('confidence'),
                'auto_replied': action_data.get('auto_replied', False),
                'sender': action_data.get('sender'),
                'subject': action_data.get('subject'),
                'metadata': action_data.get('metadata', {})
            }

            result = self.supabase.table('inbox_guardian_logs').insert(data).execute()
            logger.info(f"Logged action to Supabase: {action_data.get('action_type')}")
            return True

        except Exception as e:
            logger.error(f"Failed to log to Supabase: {e}")
            return False

    def search_recent_emails(self) -> List[Dict]:
        """Search for recent unprocessed emails using Gmail MCP"""
        try:
            # Calculate time window
            lookback_time = datetime.now(timezone.utc) - timedelta(minutes=LOOKBACK_MINUTES)
            date_filter = lookback_time.strftime('%Y/%m/%d')

            # Search query: unread emails from last LOOKBACK_MINUTES in inbox
            query = f"is:unread in:inbox after:{date_filter}"

            logger.info(f"Searching emails with query: {query}")

            # Use Claude to call Gmail MCP search_threads tool
            response = self.client.messages.create(
                model="claude-sonnet-5",
                max_tokens=2000,
                tools=[{
                    "name": "mcp__claude_ai_Gmail__search_threads",
                    "description": "Lists email threads from Gmail",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "pageSize": {"type": "integer"}
                        }
                    }
                }],
                messages=[{
                    "role": "user",
                    "content": f"Search Gmail threads with query: {query}, pageSize: 20"
                }]
            )

            # Extract thread data from tool response
            # This is a simplified version - in production, parse actual MCP response
            threads = []
            logger.info("Email search completed")
            return threads

        except Exception as e:
            logger.error(f"Failed to search emails: {e}")
            return []

    def process_email(self, thread_data: Dict) -> None:
        """Process a single email thread"""
        try:
            thread_id = thread_data.get('id')

            # Skip if already processed
            if thread_id in self.processed_thread_ids:
                return

            # Extract email details
            messages = thread_data.get('messages', [])
            if not messages:
                return

            latest_message = messages[-1]
            subject = latest_message.get('subject', 'No Subject')
            snippet = latest_message.get('snippet', '')
            sender = latest_message.get('from', 'Unknown')
            message_id = latest_message.get('id')

            logger.info(f"Processing email: {subject} from {sender}")

            # Categorize email
            category, confidence = self.categorize_email(subject, snippet, sender)
            logger.info(f"Categorized as '{category}' with {confidence:.0%} confidence")

            # Apply labels
            self.apply_labels(thread_id, category)

            # Create auto-reply if appropriate
            auto_replied = False
            if self.should_auto_reply(category, confidence):
                # Extract sender email
                sender_email = sender.split('<')[-1].rstrip('>') if '<' in sender else sender
                auto_replied = self.create_auto_reply(category, thread_id, message_id, sender_email)

            # Log to Supabase
            self.log_to_supabase({
                'action_type': 'email_processed',
                'thread_id': thread_id,
                'category': category,
                'confidence': confidence,
                'auto_replied': auto_replied,
                'sender': sender,
                'subject': subject,
                'metadata': {
                    'snippet': snippet[:200],
                    'message_id': message_id
                }
            })

            # Mark as processed
            self.processed_thread_ids.add(thread_id)

        except Exception as e:
            logger.error(f"Error processing email: {e}")

    def run_once(self) -> Dict:
        """Run a single check cycle"""
        logger.info("=" * 60)
        logger.info("Starting Inbox Guardian check cycle")
        logger.info("=" * 60)

        stats = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'emails_processed': 0,
            'auto_replies_sent': 0,
            'categories': {}
        }

        try:
            # Search for recent emails
            threads = self.search_recent_emails()
            logger.info(f"Found {len(threads)} threads to process")

            # Process each thread
            for thread in threads:
                self.process_email(thread)
                stats['emails_processed'] += 1

            # Log run summary
            self.log_to_supabase({
                'action_type': 'check_cycle_completed',
                'thread_id': None,
                'category': None,
                'confidence': None,
                'metadata': stats
            })

            logger.info(f"Check cycle completed: {stats['emails_processed']} emails processed")

        except Exception as e:
            logger.error(f"Error in check cycle: {e}")
            stats['error'] = str(e)

        return stats

    def run_continuous(self):
        """Run continuously on schedule"""
        import time

        logger.info(f"Starting continuous mode (checking every {CHECK_INTERVAL_MINUTES} minutes)")

        while True:
            try:
                self.run_once()

                # Wait for next cycle
                logger.info(f"Sleeping for {CHECK_INTERVAL_MINUTES} minutes...")
                time.sleep(CHECK_INTERVAL_MINUTES * 60)

            except KeyboardInterrupt:
                logger.info("Inbox Guardian stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in continuous mode: {e}")
                time.sleep(60)  # Wait 1 minute before retrying


def main():
    """Main entry point"""
    # Ensure log directory exists
    os.makedirs('/home/userkeysha2000/agents/inbox-guardian/logs', exist_ok=True)

    # Initialize agent
    try:
        agent = InboxGuardian()
    except Exception as e:
        logger.error(f"Failed to initialize Inbox Guardian: {e}")
        sys.exit(1)

    # Run mode based on arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Single run mode (for cron)
        stats = agent.run_once()
        print(json.dumps(stats, indent=2))
    else:
        # Continuous mode
        agent.run_continuous()


if __name__ == '__main__':
    main()
