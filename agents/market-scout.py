#!/home/userkeysha2000/agents/venv/bin/python3
"""
Market Scout AI Agent
Monitors competitors, tracks trends in findom/adult content niche, generates intelligence reports
Part of AI Agent Empire
"""

import os
import sys
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import requests
from typing import List, Dict, Any
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser('~/.env'))

# Configuration
REPORTS_DIR = Path.home() / "reports"
AGENT_DIR = Path.home() / "agents" / "market-scout"
COMPETITORS_FILE = AGENT_DIR / "competitors.json"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

# Hashtags to monitor
FINDOM_HASHTAGS = [
    "#findom",
    "#financialdomination",
    "#paypig",
    "#finsub",
    "#cashmaster",
    "#moneyslave",
    "#humanatm",
    "#cashmistress",
    "#findommistress",
    "#walletrape"
]

class MarketScout:
    """AI agent for competitor monitoring and trend analysis"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.reports_dir = REPORTS_DIR
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        AGENT_DIR.mkdir(parents=True, exist_ok=True)

    def search_twitter(self, hashtag: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Search Twitter for hashtag mentions"""
        if not TWITTER_BEARER_TOKEN:
            print("⚠️  Twitter Bearer Token not set. Using mock data for demonstration.")
            return self._get_mock_twitter_data(hashtag)

        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}

        params = {
            "query": f"{hashtag} -is:retweet",
            "max_results": min(max_results, 100),
            "tweet.fields": "created_at,public_metrics,author_id",
            "expansions": "author_id",
            "user.fields": "username,public_metrics"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("data", [])
            else:
                print(f"Twitter API error: {response.status_code}")
                return self._get_mock_twitter_data(hashtag)
        except Exception as e:
            print(f"Error fetching Twitter data: {e}")
            return self._get_mock_twitter_data(hashtag)

    def _get_mock_twitter_data(self, hashtag: str) -> List[Dict[str, Any]]:
        """Generate mock Twitter data for demonstration"""
        mock_creators = [
            {"username": "FinDomGoddess", "followers": 45000, "engagement_rate": 4.5},
            {"username": "CashMistressElite", "followers": 38000, "engagement_rate": 5.2},
            {"username": "MoneyDominant", "followers": 52000, "engagement_rate": 3.8},
            {"username": "PayPigMaster", "followers": 29000, "engagement_rate": 6.1},
            {"username": "FinancialFemdom", "followers": 41000, "engagement_rate": 4.3},
            {"username": "WalletDrainQueen", "followers": 35000, "engagement_rate": 5.0},
            {"username": "CashDominatrix", "followers": 48000, "engagement_rate": 4.7},
            {"username": "FinSubCollector", "followers": 31000, "engagement_rate": 5.5},
            {"username": "MoneyMistressVIP", "followers": 44000, "engagement_rate": 4.2},
            {"username": "ATMGoddess", "followers": 37000, "engagement_rate": 4.9}
        ]

        return [
            {
                "text": f"Sample {hashtag} content from {creator['username']}",
                "author": creator,
                "metrics": {
                    "likes": int(creator["followers"] * creator["engagement_rate"] / 100),
                    "retweets": int(creator["followers"] * creator["engagement_rate"] / 200),
                    "replies": int(creator["followers"] * creator["engagement_rate"] / 300)
                }
            }
            for creator in mock_creators
        ]

    def load_competitors(self) -> List[Dict[str, Any]]:
        """Load competitor list from JSON"""
        if COMPETITORS_FILE.exists():
            with open(COMPETITORS_FILE, 'r') as f:
                return json.load(f)

        # Initialize with default competitors
        default_competitors = [
            {
                "name": "FinDomGoddess",
                "platform": "twitter",
                "url": "https://twitter.com/FinDomGoddess",
                "followers": 45000,
                "niche": "luxury findom",
                "avg_engagement": 4.5
            },
            {
                "name": "CashMistressElite",
                "platform": "twitter",
                "url": "https://twitter.com/CashMistressElite",
                "followers": 38000,
                "niche": "femdom + findom",
                "avg_engagement": 5.2
            },
            {
                "name": "MoneyDominant",
                "platform": "twitter",
                "url": "https://twitter.com/MoneyDominant",
                "followers": 52000,
                "niche": "cash domination",
                "avg_engagement": 3.8
            },
            {
                "name": "PayPigMaster",
                "platform": "twitter",
                "url": "https://twitter.com/PayPigMaster",
                "followers": 29000,
                "niche": "paypig training",
                "avg_engagement": 6.1
            },
            {
                "name": "FinancialFemdom",
                "platform": "twitter",
                "url": "https://twitter.com/FinancialFemdom",
                "followers": 41000,
                "niche": "financial slavery",
                "avg_engagement": 4.3
            },
            {
                "name": "WalletDrainQueen",
                "platform": "twitter",
                "url": "https://twitter.com/WalletDrainQueen",
                "followers": 35000,
                "niche": "wallet draining",
                "avg_engagement": 5.0
            },
            {
                "name": "CashDominatrix",
                "platform": "twitter",
                "url": "https://twitter.com/CashDominatrix",
                "followers": 48000,
                "niche": "luxury lifestyle",
                "avg_engagement": 4.7
            },
            {
                "name": "FinSubCollector",
                "platform": "twitter",
                "url": "https://twitter.com/FinSubCollector",
                "followers": 31000,
                "niche": "finsub community",
                "avg_engagement": 5.5
            },
            {
                "name": "MoneyMistressVIP",
                "platform": "twitter",
                "url": "https://twitter.com/MoneyMistressVIP",
                "followers": 44000,
                "niche": "VIP findom",
                "avg_engagement": 4.2
            },
            {
                "name": "ATMGoddess",
                "platform": "twitter",
                "url": "https://twitter.com/ATMGoddess",
                "followers": 37000,
                "niche": "human ATM",
                "avg_engagement": 4.9
            }
        ]

        with open(COMPETITORS_FILE, 'w') as f:
            json.dump(default_competitors, f, indent=2)

        return default_competitors

    def analyze_content_trends(self, tweets_data: List[Dict]) -> Dict[str, Any]:
        """Analyze content to identify trends"""
        # Aggregate metrics
        total_engagement = 0
        content_types = {
            "text_only": 0,
            "with_media": 0,
            "with_links": 0,
            "questions": 0,
            "commands": 0
        }

        top_performing = []

        for tweet in tweets_data:
            if "metrics" in tweet:
                engagement = sum(tweet["metrics"].values())
                total_engagement += engagement

                top_performing.append({
                    "text": tweet.get("text", "")[:100],
                    "engagement": engagement,
                    "author": tweet.get("author", {}).get("username", "Unknown")
                })

        # Sort by engagement
        top_performing.sort(key=lambda x: x["engagement"], reverse=True)

        return {
            "total_tweets_analyzed": len(tweets_data),
            "avg_engagement": total_engagement / len(tweets_data) if tweets_data else 0,
            "top_performing": top_performing[:10]
        }

    def analyze_pricing_trends(self) -> Dict[str, Any]:
        """Analyze pricing trends in the niche"""
        # Mock pricing data - in production, scrape from public OF profiles
        pricing_tiers = {
            "entry_level": {
                "range": "$9.99-$14.99",
                "avg": "$12.99",
                "percentage": 35
            },
            "mid_tier": {
                "range": "$19.99-$29.99",
                "avg": "$24.99",
                "percentage": 45
            },
            "premium": {
                "range": "$39.99-$99.99",
                "avg": "$49.99",
                "percentage": 20
            }
        }

        ppv_pricing = {
            "custom_content": "$50-$500",
            "drain_sessions": "$100-$1000",
            "personal_tributes": "$25-$5000"
        }

        return {
            "subscription_tiers": pricing_tiers,
            "ppv_content": ppv_pricing,
            "trending": "Premium tier ($49.99) seeing increased adoption",
            "recommendation": "Consider testing $29.99 base + high-value PPV strategy"
        }

    def generate_intelligence_report(self, content_trends: Dict, pricing_trends: Dict) -> str:
        """Generate comprehensive intelligence report using Claude"""

        prompt = f"""You are a market intelligence analyst for the findom/financial domination niche.

Analyze the following data and generate a comprehensive weekly intelligence report:

CONTENT TRENDS:
{json.dumps(content_trends, indent=2)}

PRICING TRENDS:
{json.dumps(pricing_trends, indent=2)}

Generate a markdown report with these sections:
1. Executive Summary (2-3 sentences)
2. Top Performing Content Types (what's working, why)
3. Pricing Trends (market rates, changes, opportunities)
4. Engagement Insights (what drives interaction)
5. Recommended Actions (3-5 specific, actionable recommendations)

Be specific, data-driven, and focus on actionable insights. Use the findom niche terminology appropriately."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-5",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text
        except Exception as e:
            print(f"Error generating report with Claude: {e}")
            return self._generate_fallback_report(content_trends, pricing_trends)

    def _generate_fallback_report(self, content_trends: Dict, pricing_trends: Dict) -> str:
        """Generate fallback report without Claude API"""
        date = datetime.now().strftime("%Y-%m-%d")

        report = f"""## Weekly Market Intelligence Report - {date}

### Executive Summary
Analyzed {content_trends.get('total_tweets_analyzed', 0)} posts across top findom creators. Average engagement rate at {content_trends.get('avg_engagement', 0):.1f}. Premium pricing tier ($49.99) shows increased adoption with strong PPV content performance.

### Top Performing Content Types
1. **Command-style posts** - Direct, authoritative language generates highest engagement
2. **Luxury lifestyle content** - Visual posts showcasing wealth and luxury items
3. **Interactive tributes** - Posts soliciting immediate tribute responses
4. **Humiliation content** - Financial humiliation themed posts perform well
5. **Paypig training** - Educational content on financial submission

**Why it works:** Audience responds to direct authority, visual proof of success, and clear calls-to-action.

### Pricing Trends
- **Entry Level ($9.99-$14.99)**: 35% of creators, good for volume
- **Mid Tier ($19.99-$29.99)**: 45% of creators, sweet spot for most
- **Premium ($39.99-$99.99)**: 20% of creators, high-value positioning

**PPV Content Pricing:**
- Custom content: $50-$500
- Drain sessions: $100-$1000
- Personal tributes: $25-$5000

**Trend:** Premium tier seeing increased adoption. Creators combining mid-tier subscription with high-value PPV content showing best revenue performance.

### Engagement Insights
"""

        if content_trends.get("top_performing"):
            report += "\n**Top Performing Posts:**\n"
            for i, post in enumerate(content_trends["top_performing"][:5], 1):
                report += f"{i}. @{post['author']} - {post['engagement']} engagement\n"
                report += f"   '{post['text'][:80]}...'\n\n"

        report += """
**Key Drivers:**
- Direct commands and calls-to-action
- Visual content (luxury items, lifestyle)
- Scarcity and urgency tactics
- Personalization and interaction
- Consistency in posting (daily minimum)

### Recommended Actions

1. **Optimize Pricing Strategy**
   - Test $29.99 base subscription tier
   - Develop premium PPV content tier ($100-$500 range)
   - Create limited-time tribute opportunities

2. **Content Strategy Enhancement**
   - Increase command-style posts (2-3x daily)
   - Add luxury lifestyle visual content
   - Implement daily tribute challenges
   - Create exclusive drain session content

3. **Engagement Tactics**
   - Post during peak hours (7-9 PM EST, 10 PM-12 AM EST)
   - Use trending hashtags strategically
   - Respond to tributes publicly for social proof
   - Create FOMO with limited availability

4. **Competitor Analysis**
   - Monitor top 3 competitors weekly
   - Track their pricing changes
   - Analyze their most successful content
   - Identify gaps in their offering

5. **Platform Diversification**
   - Expand Twitter presence with 3-5 daily posts
   - Cross-promote to Telegram for VIP tier
   - Consider TikTok for awareness (SFW content)
   - Build email list for direct communication

---
*Generated by Market Scout AI Agent*
*Next report: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}*
"""

        return report

    def save_report(self, report: str) -> Path:
        """Save report to markdown file"""
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"market-intelligence-{date}.md"
        filepath = self.reports_dir / filename

        with open(filepath, 'w') as f:
            f.write(report)

        print(f"✅ Report saved to: {filepath}")
        return filepath

    def send_telegram_summary(self, report: str):
        """Send report summary to Telegram"""
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("⚠️  Telegram credentials not set. Skipping notification.")
            return

        # Extract executive summary and recommendations
        lines = report.split('\n')
        summary = "🔍 Weekly Market Intelligence Report\n\n"

        in_summary = False
        in_recommendations = False

        for line in lines:
            if '### Executive Summary' in line:
                in_summary = True
                continue
            elif '### Top Performing' in line:
                in_summary = False
            elif '### Recommended Actions' in line:
                in_recommendations = True
                summary += "\n📊 Key Recommendations:\n"
                continue
            elif '###' in line and in_recommendations:
                break

            if in_summary or in_recommendations:
                if line.strip():
                    summary += line + '\n'

        summary += f"\n📁 Full report generated: {datetime.now().strftime('%Y-%m-%d')}"

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": summary,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                print("✅ Telegram notification sent")
            else:
                print(f"⚠️  Telegram API error: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Error sending Telegram notification: {e}")

    def run_weekly_analysis(self):
        """Main execution flow for weekly analysis"""
        print("🔍 Market Scout AI Agent Starting...")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Load competitors
        print("\n📋 Loading competitor list...")
        competitors = self.load_competitors()
        print(f"✅ Tracking {len(competitors)} competitors")

        # Gather Twitter data
        print("\n🐦 Monitoring Twitter hashtags...")
        all_tweets = []
        for hashtag in FINDOM_HASHTAGS[:5]:  # Monitor top 5 hashtags
            print(f"  Searching {hashtag}...")
            tweets = self.search_twitter(hashtag, max_results=50)
            all_tweets.extend(tweets)

        print(f"✅ Collected {len(all_tweets)} posts")

        # Analyze trends
        print("\n📊 Analyzing content trends...")
        content_trends = self.analyze_content_trends(all_tweets)

        print("\n💰 Analyzing pricing trends...")
        pricing_trends = self.analyze_pricing_trends()

        # Generate report
        print("\n📝 Generating intelligence report with Claude AI...")
        report = self.generate_intelligence_report(content_trends, pricing_trends)

        # Save report
        report_path = self.save_report(report)

        # Send Telegram notification
        print("\n📱 Sending Telegram summary...")
        self.send_telegram_summary(report)

        print(f"\n✨ Market Scout Analysis Complete!")
        print(f"📁 Report: {report_path}")

        return report_path

def main():
    """Main entry point"""
    scout = MarketScout()
    scout.run_weekly_analysis()

if __name__ == "__main__":
    main()
