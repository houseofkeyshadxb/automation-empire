#!/usr/bin/env python3
"""
Content Engine AI Agent
Generates daily social media content for Mistress Keysha and Cum Slut Becky
"""

import os
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
import anthropic
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser('~/.env'))

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-key-here")
CONTENT_QUEUE_DIR = Path.home() / "content-queue"
TIMEZONE_OFFSET = 4  # Dubai is UTC+4

# Initialize clients
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL != "https://your-project.supabase.co" else None

# Persona configurations
PERSONAS = {
    "keysha": {
        "full_name": "Mistress Keysha",
        "tone": "dominant, commanding, luxury",
        "voice": "Superior, sophisticated, authoritative. Uses wealth and power language.",
        "hashtags_instagram": ["#findom", "#paypig", "#moneyslave", "#financialdomination", "#luxurylifestyle"],
        "hashtags_twitter": ["#findom", "#paypig", "#finsub", "#humanatm"],
        "hashtags_tiktok": ["#findom", "#luxurylifestyle", "#dubai", "#mistress"],
        "cta": "Session bookings open - link in bio",
        "emojis": ["👑", "💋", "💎", "💰", "🔥"]
    },
    "becky": {
        "full_name": "Cum Slut Becky",
        "tone": "submissive, eager, playful",
        "voice": "Sweet, grateful, enthusiastic. Shows appreciation and eagerness.",
        "hashtags_instagram": ["#goodgirl", "#obedient", "#contentcreator", "#spicycontent"],
        "hashtags_twitter": ["#contentcreator", "#spicy", "#subscribe"],
        "hashtags_tiktok": ["#contentcreator", "#spicy", "#behindthescenes"],
        "cta": "More content in bio - subscribe to see everything",
        "emojis": ["💦", "😈", "💕", "🎀", "✨"]
    }
}

# Content templates
CONTENT_THEMES = {
    "keysha": {
        "power": [
            "Your wallet looks heavy. Let me lighten that burden for you",
            "Tributes aren't optional. They're expected",
            "I don't chase. I attract. And you will pay for the privilege",
            "Watching you drain your account for me never gets old",
            "Good boys know their place: beneath my heels and behind their wallets"
        ],
        "lifestyle": [
            "Shopping on your dime hits different",
            "Another tribute, another designer bag. Keep them coming",
            "Living my best life while you fund it. As it should be",
            "Your hard work pays for my soft life. Thank you for your service",
            "Luxury isn't a choice. It's a requirement. You understand, don't you?"
        ],
        "sessions": [
            "Session slots filling fast. DM if you're worthy of my time",
            "Taking bookings for this week. Deposits mandatory, time wasters blocked",
            "Limited availability this month. Prove you deserve a spot",
            "New session packages available. Your wallet is about to get lighter",
            "Book now or watch someone else take your spot. I don't wait"
        ],
        "teaser": [
            "New content dropping tonight. Subscribers get first access",
            "Behind the scenes of today's photoshoot. Link in bio for full sets",
            "Sneak peek at this week's premium content. You know what to do",
            "Fresh content coming to OnlyFans. Don't miss out",
            "This week's exclusive content is going to drain you. In every way"
        ]
    },
    "becky": {
        "grateful": [
            "Thank you for all the tributes today! You're the best subs ever",
            "Mistress says I've been a good girl. Thanks for helping me please her",
            "So grateful for all your support! More content coming soon",
            "You guys spoil me! New content dropping tonight as a thank you",
            "Feeling blessed by all your kindness today"
        ],
        "eager": [
            "Just finished editing new content for you! Mistress approved it",
            "Can't wait to show you what we filmed today",
            "Working on something special for my favorite subscribers",
            "New photoshoot coming soon! So excited to share",
            "Behind the scenes content uploading now. Check bio for link"
        ],
        "playful": [
            "Mistress caught me being naughty today... again",
            "Guess what Mistress has me doing tomorrow? Subscribers will find out first",
            "Training continues... and you get to watch",
            "Oops, did I tease too much? More in bio",
            "Being a good girl has its perks. Want to see?"
        ],
        "content": [
            "New video just dropped! Link in bio for full access",
            "This week's content is 🔥 Subscribe to see it all",
            "Just uploaded 3 new sets. Thank you for your continued support",
            "Exclusive content available now. You don't want to miss this",
            "Fresh content alert! Check bio for instant access"
        ]
    }
}

def get_dubai_time():
    """Get current Dubai time (UTC+4)"""
    utc_now = datetime.now(timezone.utc)
    dubai_time = utc_now + timedelta(hours=TIMEZONE_OFFSET)
    return dubai_time

def generate_content_with_claude(persona_name: str, platform: str, theme: str = None) -> str:
    """Generate content using Claude AI"""
    if not claude:
        # Fallback to templates if no API key
        return generate_template_content(persona_name, platform, theme)

    persona = PERSONAS[persona_name]

    prompt = f"""You are generating social media content for {persona['full_name']}.

PERSONA CHARACTERISTICS:
- Tone: {persona['tone']}
- Voice: {persona['voice']}

PLATFORM: {platform.upper()}
THEME: {theme if theme else 'general engagement'}

REQUIREMENTS:
- Keep it authentic to the character
- {"Instagram: 1-2 sentences max, include emojis" if platform == "instagram" else ""}
- {"Twitter: Under 280 characters, punchy and engaging" if platform == "twitter" else ""}
- {"TikTok: Short caption, hook-focused, trending-friendly" if platform == "tiktok" else ""}
- Include call-to-action: {persona['cta']}
- Use 2-3 relevant emojis from: {', '.join(persona['emojis'])}
- DO NOT include hashtags (they'll be added separately)

Generate ONE social media caption now:"""

    try:
        message = claude.messages.create(
            model="claude-sonnet-5",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        print(f"Claude API error: {e}")
        return generate_template_content(persona_name, platform, theme)

def generate_template_content(persona_name: str, platform: str, theme: str = None) -> str:
    """Fallback template-based content generation"""
    persona = PERSONAS[persona_name]

    if theme and theme in CONTENT_THEMES[persona_name]:
        base_content = random.choice(CONTENT_THEMES[persona_name][theme])
    else:
        # Pick random theme
        available_themes = list(CONTENT_THEMES[persona_name].keys())
        random_theme = random.choice(available_themes)
        base_content = random.choice(CONTENT_THEMES[persona_name][random_theme])

    # Add emojis
    emoji = random.choice(persona['emojis'])

    if platform == "instagram":
        return f"{base_content} {emoji} {persona['cta']}"
    elif platform == "twitter":
        return f"{base_content} {emoji}"
    else:  # tiktok
        return f"{base_content} {emoji}"

def generate_hashtags(persona_name: str, platform: str, count: int = 5) -> list:
    """Generate hashtags for platform"""
    persona = PERSONAS[persona_name]
    hashtag_key = f"hashtags_{platform}"

    if hashtag_key in persona:
        base_tags = persona[hashtag_key].copy()
        random.shuffle(base_tags)
        return base_tags[:count]

    return []

def save_content_to_file(persona_name: str, platform: str, content: str, hashtags: list):
    """Save generated content to file with timestamp"""
    dubai_time = get_dubai_time()
    timestamp = dubai_time.strftime("%Y%m%d_%H%M%S")

    filename = f"{timestamp}_{persona_name}_{platform}.json"
    filepath = CONTENT_QUEUE_DIR / filename

    content_data = {
        "persona": persona_name,
        "platform": platform,
        "content": content,
        "hashtags": hashtags,
        "full_caption": f"{content}\n\n{' '.join(hashtags)}" if hashtags else content,
        "generated_at": dubai_time.isoformat(),
        "status": "pending"
    }

    with open(filepath, 'w') as f:
        json.dump(content_data, f, indent=2)

    print(f"✅ Saved: {filename}")
    return filepath

def log_to_supabase(persona_name: str, platform: str, content: str, hashtags: list):
    """Log content to Supabase database"""
    if not supabase:
        print("⚠️  Supabase not configured, skipping database logging")
        return

    try:
        dubai_time = get_dubai_time()

        data = {
            "persona": persona_name,
            "platform": platform,
            "content": content,
            "hashtags": hashtags,
            "full_caption": f"{content}\n\n{' '.join(hashtags)}" if hashtags else content,
            "generated_at": dubai_time.isoformat(),
            "status": "pending",
            "posted": False
        }

        # Create table if doesn't exist
        supabase.table("content_posts").insert(data).execute()
        print(f"✅ Logged to Supabase: {persona_name} - {platform}")

    except Exception as e:
        print(f"⚠️  Supabase logging error: {e}")

def generate_daily_content():
    """Generate all daily content according to schedule"""
    dubai_time = get_dubai_time()
    current_hour = dubai_time.hour

    print(f"\n{'='*60}")
    print(f"🤖 CONTENT ENGINE - {dubai_time.strftime('%Y-%m-%d %H:%M')} Dubai Time")
    print(f"{'='*60}\n")

    # Determine which persona (alternate daily)
    day_of_year = dubai_time.timetuple().tm_yday
    primary_persona = "keysha" if day_of_year % 2 == 0 else "becky"
    secondary_persona = "becky" if primary_persona == "keysha" else "keysha"

    print(f"📋 Today's primary persona: {PERSONAS[primary_persona]['full_name']}")
    print(f"📋 Secondary persona: {PERSONAS[secondary_persona]['full_name']}\n")

    content_generated = []

    # Schedule-based content generation
    # Instagram: 10am & 6pm Dubai time
    if current_hour in [10, 18]:
        print("📸 INSTAGRAM POST TIME")
        for persona in [primary_persona, secondary_persona]:
            theme = random.choice(list(CONTENT_THEMES[persona].keys()))
            content = generate_content_with_claude(persona, "instagram", theme)
            hashtags = generate_hashtags(persona, "instagram", 5)

            filepath = save_content_to_file(persona, "instagram", content, hashtags)
            log_to_supabase(persona, "instagram", content, hashtags)

            print(f"\n{PERSONAS[persona]['full_name']} - Instagram:")
            print(f"{content}")
            print(f"{' '.join(hashtags)}\n")

            content_generated.append({
                "persona": persona,
                "platform": "instagram",
                "content": content,
                "hashtags": hashtags,
                "file": str(filepath)
            })

    # Twitter: Every 2 hours
    if current_hour % 2 == 0:
        print("🐦 TWITTER POST TIME")
        persona = primary_persona if current_hour % 4 == 0 else secondary_persona
        theme = random.choice(list(CONTENT_THEMES[persona].keys()))
        content = generate_content_with_claude(persona, "twitter", theme)
        hashtags = generate_hashtags(persona, "twitter", 3)

        filepath = save_content_to_file(persona, "twitter", content, hashtags)
        log_to_supabase(persona, "twitter", content, hashtags)

        print(f"\n{PERSONAS[persona]['full_name']} - Twitter:")
        print(f"{content}")
        print(f"{' '.join(hashtags)}\n")

        content_generated.append({
            "persona": persona,
            "platform": "twitter",
            "content": content,
            "hashtags": hashtags,
            "file": str(filepath)
        })

    # TikTok: 12pm & 8pm Dubai time
    if current_hour in [12, 20]:
        print("🎵 TIKTOK CAPTION TIME")
        for persona in [primary_persona, secondary_persona]:
            theme = random.choice(list(CONTENT_THEMES[persona].keys()))
            content = generate_content_with_claude(persona, "tiktok", theme)
            hashtags = generate_hashtags(persona, "tiktok", 5)

            filepath = save_content_to_file(persona, "tiktok", content, hashtags)
            log_to_supabase(persona, "tiktok", content, hashtags)

            print(f"\n{PERSONAS[persona]['full_name']} - TikTok:")
            print(f"{content}")
            print(f"{' '.join(hashtags)}\n")

            content_generated.append({
                "persona": persona,
                "platform": "tiktok",
                "content": content,
                "hashtags": hashtags,
                "file": str(filepath)
            })

    print(f"\n{'='*60}")
    print(f"✅ Generated {len(content_generated)} pieces of content")
    print(f"📁 Saved to: {CONTENT_QUEUE_DIR}")
    print(f"{'='*60}\n")

    return content_generated

def test_generation():
    """Test content generation for all platforms and personas"""
    print("\n🧪 TESTING CONTENT GENERATION\n")

    for persona_name in ["keysha", "becky"]:
        print(f"\n{'='*60}")
        print(f"Testing: {PERSONAS[persona_name]['full_name']}")
        print(f"{'='*60}\n")

        for platform in ["instagram", "twitter", "tiktok"]:
            print(f"\n📱 {platform.upper()}:")
            content = generate_content_with_claude(persona_name, platform)
            hashtags = generate_hashtags(persona_name, platform)

            print(f"{content}")
            print(f"{' '.join(hashtags)}")
            print(f"\nFull caption:\n{content}\n\n{' '.join(hashtags)}\n")

            save_content_to_file(persona_name, platform, content, hashtags)

if __name__ == "__main__":
    import sys

    # Ensure content queue directory exists
    CONTENT_QUEUE_DIR.mkdir(exist_ok=True)

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_generation()
    else:
        generate_daily_content()
