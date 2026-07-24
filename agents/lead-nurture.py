#!/usr/bin/env python3
"""
Lead Nurture Bot - AI Agent Empire
21-day automated follow-up sequences for OnlyFans subscribers

Tracks subscribers, sends automated DM sequences, and logs all interactions
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
from supabase import create_client, Client
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser('~/.env'))

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
FANVUE_API_KEY = os.getenv("FANVUE_API_KEY", "")

# Initialize clients
supabase = None
if SUPABASE_URL and SUPABASE_KEY and not SUPABASE_URL.startswith("https://placeholder"):
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"⚠️  Supabase connection failed: {e}")
        print("Running in standalone mode without database logging")

anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)


# 21-Day Message Sequence
NURTURE_SEQUENCE = {
    1: {
        "type": "welcome",
        "message": "Welcome baby 💋 I'm so glad you subscribed. You're going to LOVE what I have planned for you. Check your DMs daily - I always reward my loyal subs 😈",
        "goal": "introduce_yourself"
    },
    3: {
        "type": "ppv_offer",
        "message": "I just posted some VERY naughty content in my PPV section... first 5 buyers get 20% off 💦 Interested?",
        "goal": "ppv_sale",
        "upsell": "ppv_content"
    },
    5: {
        "type": "personalization",
        "message": "Hey babe 😘 I want to make sure I'm giving you exactly what you want. What type of content gets you going the most? Solo? B/G? Toys? Tell me your fantasies 🔥",
        "goal": "collect_preferences"
    },
    7: {
        "type": "custom_video",
        "message": "I'm taking custom video requests this week! 💖 5 min solo video: $50 | 10 min solo: $80 | 5 min B/G: $100 | Want to see yourself in my next video? DM me your idea 😈",
        "goal": "custom_video_sale",
        "upsell": "custom_videos"
    },
    10: {
        "type": "sexting_session",
        "message": "I'm feeling extra naughty tonight 😈 Want to have some fun? I'm offering live sexting sessions: 15 min - $30 | 30 min - $50 | 60 min - $80. Real-time pics/vids included 💦 Available NOW",
        "goal": "sexting_sale",
        "upsell": "sexting_sessions"
    },
    14: {
        "type": "dick_rating",
        "message": "I LOVE rating cocks 🍆 Send me a pic and I'll give you an honest rating (or SPH if that's your thing 😏) Video dick rating: $20 | Written detailed rating: $15 | Want me to worship it? Let's talk 💋",
        "goal": "dick_rating_sale",
        "upsell": "dick_ratings"
    },
    17: {
        "type": "relationship_building",
        "message": "Just wanted to check in with my favorite sub 💖 How are you enjoying the content so far? Any special requests? I love hearing from you, makes me feel so special 🥰",
        "goal": "build_relationship"
    },
    21: {
        "type": "vip_upsell",
        "message": "You've been such an amazing supporter 😍 I want to offer you VIP access to my exclusive tier - daily personal messages, priority custom content, exclusive XXX videos, and direct access to me 24/7. Only $99/month. Want to be my VIP baby? 👑",
        "goal": "vip_conversion",
        "upsell": "vip_tier"
    }
}


class LeadNurtureBot:
    """AI agent for nurturing OnlyFans subscribers through automated sequences"""

    def __init__(self):
        self.supabase = supabase
        self.anthropic = anthropic

    def get_new_subscribers(self) -> List[Dict[str, Any]]:
        """Fetch subscribers who need nurturing messages today"""
        try:
            response = self.supabase.table("subscribers").select("*").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching subscribers: {e}")
            return []

    def calculate_day_in_sequence(self, subscribe_date: str) -> int:
        """Calculate which day in the 21-day sequence the subscriber is on"""
        sub_date = datetime.fromisoformat(subscribe_date.replace('Z', '+00:00'))
        days_since_sub = (datetime.now() - sub_date).days + 1
        return days_since_sub

    def get_last_message_sent(self, subscriber_id: str) -> Optional[int]:
        """Get the last sequence day message sent to this subscriber"""
        try:
            response = self.supabase.table("lead_nurture_log").select("sequence_day").eq(
                "subscriber_id", subscriber_id
            ).order("sent_at", desc=True).limit(1).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]["sequence_day"]
            return None
        except Exception as e:
            print(f"Error fetching last message: {e}")
            return None

    def personalize_message(self, template: str, subscriber: Dict[str, Any]) -> str:
        """Use Claude to personalize the message based on subscriber data"""
        try:
            # Get subscriber preferences and history
            preferences = subscriber.get("preferences", {})
            purchase_history = subscriber.get("purchase_history", [])
            engagement_level = subscriber.get("engagement_level", "medium")

            prompt = f"""You are an OnlyFans creator sending a personalized DM to a subscriber.

Subscriber info:
- Name/Username: {subscriber.get('username', 'babe')}
- Days subscribed: {self.calculate_day_in_sequence(subscriber.get('subscribed_at', datetime.now().isoformat()))}
- Preferences: {json.dumps(preferences)}
- Past purchases: {json.dumps(purchase_history)}
- Engagement level: {engagement_level}

Message template: "{template}"

Personalize this message to feel authentic and tailored to this subscriber. Keep the flirty, seductive tone. Keep it under 200 characters if possible. Use emojis naturally.

Return ONLY the personalized message, nothing else."""

            response = self.anthropic.messages.create(
                model="claude-sonnet-5",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text.strip()
        except Exception as e:
            print(f"Error personalizing message: {e}")
            return template  # Fallback to template

    def send_dm_via_fanvue(self, subscriber_id: str, message: str) -> bool:
        """Send DM through Fanvue API (placeholder - implement when API available)"""
        if not FANVUE_API_KEY:
            print(f"[SIMULATION] Would send to {subscriber_id}: {message}")
            return True

        try:
            # TODO: Implement Fanvue API integration
            # For now, log the message
            print(f"Sending to {subscriber_id}: {message}")
            return True
        except Exception as e:
            print(f"Error sending DM: {e}")
            return False

    def log_interaction(self, subscriber_id: str, sequence_day: int,
                       message: str, sent: bool, goal: str, upsell: Optional[str] = None):
        """Log the nurture interaction to Supabase"""
        try:
            log_entry = {
                "subscriber_id": subscriber_id,
                "sequence_day": sequence_day,
                "message_sent": message,
                "sent_successfully": sent,
                "sent_at": datetime.now().isoformat(),
                "goal": goal,
                "upsell_type": upsell,
                "response_received": False,
                "converted": False
            }

            self.supabase.table("lead_nurture_log").insert(log_entry).execute()
            print(f"✅ Logged interaction for subscriber {subscriber_id} - Day {sequence_day}")
        except Exception as e:
            print(f"Error logging interaction: {e}")

    def should_send_message(self, subscriber: Dict[str, Any], current_day: int) -> bool:
        """Determine if we should send a message to this subscriber today"""
        # Check if there's a message scheduled for this day
        if current_day not in NURTURE_SEQUENCE:
            return False

        # Check if we haven't sent this day's message yet
        last_sent = self.get_last_message_sent(subscriber["id"])
        if last_sent and last_sent >= current_day:
            return False

        # Don't send if subscriber is past day 21
        if current_day > 21:
            return False

        # Don't send if subscriber has unsubscribed
        if subscriber.get("status") == "unsubscribed":
            return False

        return True

    def run_nurture_sequence(self):
        """Main function to run the nurture sequence for all subscribers"""
        print(f"\n🤖 Lead Nurture Bot - Running at {datetime.now()}")
        print("=" * 60)

        subscribers = self.get_new_subscribers()
        print(f"📊 Found {len(subscribers)} total subscribers")

        messages_sent = 0

        for subscriber in subscribers:
            subscriber_id = subscriber["id"]
            username = subscriber.get("username", "Unknown")
            subscribe_date = subscriber.get("subscribed_at")

            if not subscribe_date:
                print(f"⚠️  Skipping {username} - no subscription date")
                continue

            current_day = self.calculate_day_in_sequence(subscribe_date)

            if not self.should_send_message(subscriber, current_day):
                continue

            # Get the sequence message for this day
            sequence_msg = NURTURE_SEQUENCE.get(current_day)
            if not sequence_msg:
                continue

            print(f"\n👤 Processing: {username} (Day {current_day})")

            # Personalize the message
            base_message = sequence_msg["message"]
            personalized_message = self.personalize_message(base_message, subscriber)

            # Send the message
            sent = self.send_dm_via_fanvue(subscriber_id, personalized_message)

            # Log the interaction
            self.log_interaction(
                subscriber_id=subscriber_id,
                sequence_day=current_day,
                message=personalized_message,
                sent=sent,
                goal=sequence_msg.get("goal", ""),
                upsell=sequence_msg.get("upsell")
            )

            if sent:
                messages_sent += 1
                print(f"✉️  Sent Day {current_day} message: {sequence_msg['type']}")

        print("\n" + "=" * 60)
        print(f"✅ Nurture sequence complete - {messages_sent} messages sent")
        print(f"🕒 Finished at {datetime.now()}\n")

        return messages_sent

    def analyze_performance(self):
        """Analyze which messages convert and which subscribers buy"""
        try:
            # Get conversion stats by sequence day
            response = self.supabase.table("lead_nurture_log").select(
                "sequence_day, goal, upsell_type, converted, response_received"
            ).execute()

            if not response.data:
                print("No performance data yet")
                return

            stats = {}
            for record in response.data:
                day = record["sequence_day"]
                if day not in stats:
                    stats[day] = {
                        "sent": 0,
                        "responses": 0,
                        "conversions": 0,
                        "goal": record["goal"],
                        "upsell": record.get("upsell_type", "N/A")
                    }

                stats[day]["sent"] += 1
                if record.get("response_received"):
                    stats[day]["responses"] += 1
                if record.get("converted"):
                    stats[day]["conversions"] += 1

            # Print performance report
            print("\n📈 LEAD NURTURE PERFORMANCE REPORT")
            print("=" * 80)
            print(f"{'Day':<5} {'Type':<20} {'Sent':<8} {'Responses':<12} {'Conversions':<12} {'Conv %':<10}")
            print("-" * 80)

            for day in sorted(stats.keys()):
                s = stats[day]
                conv_rate = (s["conversions"] / s["sent"] * 100) if s["sent"] > 0 else 0
                print(f"{day:<5} {s['upsell']:<20} {s['sent']:<8} {s['responses']:<12} {s['conversions']:<12} {conv_rate:.1f}%")

            print("=" * 80 + "\n")

        except Exception as e:
            print(f"Error analyzing performance: {e}")


def main():
    """Main entry point"""
    bot = LeadNurtureBot()

    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--analyze":
        bot.analyze_performance()
    else:
        bot.run_nurture_sequence()


if __name__ == "__main__":
    main()
