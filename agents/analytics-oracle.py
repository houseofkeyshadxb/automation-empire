#!/usr/bin/env python3
"""
Analytics Oracle AI Agent
Generates weekly business reports tracking OnlyFans earnings, subscribers, PPV sales, and social engagement.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
from dataclasses import dataclass
from collections import defaultdict

# Third-party imports
try:
    from supabase import create_client, Client
    import requests
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Install with: pip install supabase requests python-dotenv matplotlib")
    sys.exit(1)

# Optional imports for charting
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False
    print("Warning: matplotlib not available. Using ASCII charts instead.")

# Load environment variables
load_dotenv()


@dataclass
class KPIMetrics:
    """Key Performance Indicators"""
    total_revenue: float = 0.0
    mrr: float = 0.0
    ppv_sales: float = 0.0
    custom_videos: float = 0.0
    tributes: float = 0.0

    mistress_keysha_subs: int = 0
    cum_slut_becky_subs: int = 0
    new_subs: int = 0
    churned_subs: int = 0
    churn_rate: float = 0.0

    twitter_followers: int = 0
    twitter_engagement_rate: float = 0.0
    instagram_followers: int = 0
    instagram_likes_per_post: int = 0
    tiktok_views: int = 0
    tiktok_new_followers: int = 0

    best_ppv_title: str = ""
    best_ppv_revenue: float = 0.0
    most_engaged_tweet: str = ""
    highest_tribute: float = 0.0

    # Week-over-week changes
    revenue_change_pct: float = 0.0
    mrr_change_pct: float = 0.0
    keysha_sub_change: int = 0
    becky_sub_change: int = 0


class AnalyticsOracle:
    """Analytics Oracle AI Agent - Weekly Business Intelligence"""

    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not all([self.supabase_url, self.supabase_key]):
            raise ValueError("Missing required environment variables: SUPABASE_URL, SUPABASE_KEY")

        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.reports_dir = os.path.expanduser("~/reports")
        os.makedirs(self.reports_dir, exist_ok=True)

    def get_date_range(self, days: int = 7) -> tuple[str, str]:
        """Get date range for the report"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return start_date.isoformat(), end_date.isoformat()

    def fetch_revenue_data(self, start_date: str, end_date: str) -> Dict[str, float]:
        """Fetch revenue data from Supabase"""
        try:
            # Query revenue table for the date range
            response = self.supabase.table("revenue").select("*").gte(
                "created_at", start_date
            ).lte("created_at", end_date).execute()

            revenue_breakdown = {
                "total": 0.0,
                "ppv": 0.0,
                "custom_videos": 0.0,
                "tributes": 0.0,
                "subscriptions": 0.0
            }

            for record in response.data:
                amount = float(record.get("amount", 0))
                revenue_type = record.get("type", "").lower()

                revenue_breakdown["total"] += amount

                if "ppv" in revenue_type:
                    revenue_breakdown["ppv"] += amount
                elif "custom" in revenue_type or "video" in revenue_type:
                    revenue_breakdown["custom_videos"] += amount
                elif "tribute" in revenue_type:
                    revenue_breakdown["tributes"] += amount
                elif "subscription" in revenue_type or "sub" in revenue_type:
                    revenue_breakdown["subscriptions"] += amount

            return revenue_breakdown

        except Exception as e:
            print(f"Error fetching revenue data: {e}")
            return {"total": 0.0, "ppv": 0.0, "custom_videos": 0.0, "tributes": 0.0, "subscriptions": 0.0}

    def fetch_subscriber_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Fetch subscriber data from Supabase"""
        try:
            # Current subscribers by account
            current_subs = self.supabase.table("subscribers").select("*").eq(
                "status", "active"
            ).execute()

            # New subscribers this week
            new_subs = self.supabase.table("subscribers").select("*").gte(
                "subscribed_at", start_date
            ).lte("subscribed_at", end_date).execute()

            # Churned subscribers this week
            churned_subs = self.supabase.table("subscribers").select("*").eq(
                "status", "churned"
            ).gte("churned_at", start_date).lte("churned_at", end_date).execute()

            # Count by account
            keysha_count = sum(1 for s in current_subs.data if s.get("account") == "mistress_keysha")
            becky_count = sum(1 for s in current_subs.data if s.get("account") == "cum_slut_becky")

            total_active = len(current_subs.data)
            new_count = len(new_subs.data)
            churned_count = len(churned_subs.data)
            churn_rate = (churned_count / total_active * 100) if total_active > 0 else 0.0

            return {
                "mistress_keysha": keysha_count,
                "cum_slut_becky": becky_count,
                "new": new_count,
                "churned": churned_count,
                "churn_rate": churn_rate,
                "total_active": total_active
            }

        except Exception as e:
            print(f"Error fetching subscriber data: {e}")
            return {
                "mistress_keysha": 0,
                "cum_slut_becky": 0,
                "new": 0,
                "churned": 0,
                "churn_rate": 0.0,
                "total_active": 0
            }

    def fetch_social_media_data(self) -> Dict[str, Any]:
        """Fetch social media metrics from Supabase"""
        try:
            # Get latest social media metrics
            twitter = self.supabase.table("social_metrics").select("*").eq(
                "platform", "twitter"
            ).order("created_at", desc=True).limit(1).execute()

            instagram = self.supabase.table("social_metrics").select("*").eq(
                "platform", "instagram"
            ).order("created_at", desc=True).limit(1).execute()

            tiktok = self.supabase.table("social_metrics").select("*").eq(
                "platform", "tiktok"
            ).order("created_at", desc=True).limit(1).execute()

            twitter_data = twitter.data[0] if twitter.data else {}
            instagram_data = instagram.data[0] if instagram.data else {}
            tiktok_data = tiktok.data[0] if tiktok.data else {}

            return {
                "twitter_followers": twitter_data.get("followers", 0),
                "twitter_engagement_rate": twitter_data.get("engagement_rate", 0.0),
                "instagram_followers": instagram_data.get("followers", 0),
                "instagram_likes_per_post": instagram_data.get("avg_likes", 0),
                "tiktok_views": tiktok_data.get("total_views", 0),
                "tiktok_new_followers": tiktok_data.get("new_followers", 0)
            }

        except Exception as e:
            print(f"Error fetching social media data: {e}")
            return {
                "twitter_followers": 0,
                "twitter_engagement_rate": 0.0,
                "instagram_followers": 0,
                "instagram_likes_per_post": 0,
                "tiktok_views": 0,
                "tiktok_new_followers": 0
            }

    def fetch_top_performers(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Fetch top performing content"""
        try:
            # Best selling PPV
            ppv = self.supabase.table("revenue").select("*").eq(
                "type", "ppv"
            ).gte("created_at", start_date).lte("created_at", end_date).order(
                "amount", desc=True
            ).limit(1).execute()

            # Most engaged tweet (from social_posts table)
            tweet = self.supabase.table("social_posts").select("*").eq(
                "platform", "twitter"
            ).gte("created_at", start_date).lte("created_at", end_date).order(
                "engagement", desc=True
            ).limit(1).execute()

            # Highest tribute
            tribute = self.supabase.table("revenue").select("*").eq(
                "type", "tribute"
            ).gte("created_at", start_date).lte("created_at", end_date).order(
                "amount", desc=True
            ).limit(1).execute()

            ppv_data = ppv.data[0] if ppv.data else {}
            tweet_data = tweet.data[0] if tweet.data else {}
            tribute_data = tribute.data[0] if tribute.data else {}

            return {
                "best_ppv_title": ppv_data.get("title", "N/A"),
                "best_ppv_revenue": ppv_data.get("amount", 0.0),
                "most_engaged_tweet": tweet_data.get("url", "N/A"),
                "highest_tribute": tribute_data.get("amount", 0.0)
            }

        except Exception as e:
            print(f"Error fetching top performers: {e}")
            return {
                "best_ppv_title": "N/A",
                "best_ppv_revenue": 0.0,
                "most_engaged_tweet": "N/A",
                "highest_tribute": 0.0
            }

    def calculate_mrr(self) -> float:
        """Calculate Monthly Recurring Revenue"""
        try:
            # Get all active subscriptions
            subs = self.supabase.table("subscribers").select("*").eq(
                "status", "active"
            ).execute()

            # Assuming $9.99 per subscription (adjust based on your pricing)
            subscription_price = 9.99
            mrr = len(subs.data) * subscription_price

            return mrr

        except Exception as e:
            print(f"Error calculating MRR: {e}")
            return 0.0

    def get_previous_week_metrics(self) -> Dict[str, float]:
        """Get previous week's metrics for comparison"""
        end_date = (datetime.now() - timedelta(days=7)).isoformat()
        start_date = (datetime.now() - timedelta(days=14)).isoformat()

        prev_revenue = self.fetch_revenue_data(start_date, end_date)
        prev_subs = self.fetch_subscriber_data(start_date, end_date)

        return {
            "revenue": prev_revenue["total"],
            "mrr": self.calculate_mrr(),  # Simplified - would need historical MRR tracking
            "keysha_subs": prev_subs["mistress_keysha"],
            "becky_subs": prev_subs["cum_slut_becky"]
        }

    def generate_kpi_metrics(self) -> KPIMetrics:
        """Generate comprehensive KPI metrics"""
        start_date, end_date = self.get_date_range(7)

        # Fetch all data
        revenue = self.fetch_revenue_data(start_date, end_date)
        subscribers = self.fetch_subscriber_data(start_date, end_date)
        social = self.fetch_social_media_data()
        top_performers = self.fetch_top_performers(start_date, end_date)
        mrr = self.calculate_mrr()

        # Get previous week for comparisons
        prev_week = self.get_previous_week_metrics()

        # Calculate changes
        revenue_change = ((revenue["total"] - prev_week["revenue"]) / prev_week["revenue"] * 100) if prev_week["revenue"] > 0 else 0.0
        mrr_change = ((mrr - prev_week["mrr"]) / prev_week["mrr"] * 100) if prev_week["mrr"] > 0 else 0.0
        keysha_change = subscribers["mistress_keysha"] - prev_week["keysha_subs"]
        becky_change = subscribers["cum_slut_becky"] - prev_week["becky_subs"]

        return KPIMetrics(
            total_revenue=revenue["total"],
            mrr=mrr,
            ppv_sales=revenue["ppv"],
            custom_videos=revenue["custom_videos"],
            tributes=revenue["tributes"],
            mistress_keysha_subs=subscribers["mistress_keysha"],
            cum_slut_becky_subs=subscribers["cum_slut_becky"],
            new_subs=subscribers["new"],
            churned_subs=subscribers["churned"],
            churn_rate=subscribers["churn_rate"],
            twitter_followers=social["twitter_followers"],
            twitter_engagement_rate=social["twitter_engagement_rate"],
            instagram_followers=social["instagram_followers"],
            instagram_likes_per_post=social["instagram_likes_per_post"],
            tiktok_views=social["tiktok_views"],
            tiktok_new_followers=social["tiktok_new_followers"],
            best_ppv_title=top_performers["best_ppv_title"],
            best_ppv_revenue=top_performers["best_ppv_revenue"],
            most_engaged_tweet=top_performers["most_engaged_tweet"],
            highest_tribute=top_performers["highest_tribute"],
            revenue_change_pct=revenue_change,
            mrr_change_pct=mrr_change,
            keysha_sub_change=keysha_change,
            becky_sub_change=becky_change
        )

    def generate_recommendations(self, metrics: KPIMetrics) -> List[str]:
        """Generate data-driven recommendations"""
        recommendations = []

        # Revenue analysis
        if metrics.revenue_change_pct < -10:
            recommendations.append(
                f"Revenue dropped by {abs(metrics.revenue_change_pct):.1f}% - Consider launching a flash PPV sale or limited-time offer to boost engagement"
            )
        elif metrics.revenue_change_pct > 20:
            recommendations.append(
                f"Revenue up {metrics.revenue_change_pct:.1f}% - Excellent week! Double down on content formats that drove this growth"
            )

        # Churn analysis
        if metrics.churn_rate > 5:
            recommendations.append(
                f"Churn rate at {metrics.churn_rate:.1f}% is concerning - Send re-engagement DMs to at-risk subscribers with exclusive content preview"
            )

        # PPV performance
        if metrics.ppv_sales > metrics.custom_videos * 2:
            recommendations.append(
                f"PPV massively outperforming custom videos (${metrics.ppv_sales:.0f} vs ${metrics.custom_videos:.0f}) - Focus on creating more PPV content this week"
            )

        # Social media growth
        if metrics.twitter_engagement_rate < 2.0:
            recommendations.append(
                f"Twitter engagement at {metrics.twitter_engagement_rate:.1f}% - Try more interactive content (polls, questions, teaser clips)"
            )

        # Subscriber growth
        if metrics.new_subs < 10:
            recommendations.append(
                f"Only {metrics.new_subs} new subs this week - Increase social media posting frequency and run a limited-time discount promo"
            )

        # MRR trends
        if metrics.mrr_change_pct < 0:
            recommendations.append(
                f"MRR declining - Launch a subscriber loyalty program or exclusive tier to retain existing fans"
            )

        # Default recommendations if none triggered
        if not recommendations:
            recommendations.append("Maintain current content strategy - all KPIs are healthy")
            recommendations.append(f"Your best PPV '{metrics.best_ppv_title}' made ${metrics.best_ppv_revenue:.0f} - create similar content")

        return recommendations

    def create_ascii_chart(self, title: str, data: Dict[str, float], max_width: int = 40) -> str:
        """Create simple ASCII bar chart"""
        if not data:
            return "No data available"

        max_value = max(data.values()) if data.values() else 1
        chart = [f"\n{title}"]
        chart.append("-" * (max_width + 20))

        for label, value in data.items():
            bar_length = int((value / max_value) * max_width) if max_value > 0 else 0
            bar = "█" * bar_length
            chart.append(f"{label:20s} | {bar} ${value:,.0f}")

        chart.append("-" * (max_width + 20))
        return "\n".join(chart)

    def generate_report(self, metrics: KPIMetrics) -> str:
        """Generate comprehensive weekly report"""
        start_date, end_date = self.get_date_range(7)
        date_range = f"{datetime.fromisoformat(start_date).strftime('%b %d')} - {datetime.fromisoformat(end_date).strftime('%b %d, %Y')}"

        recommendations = self.generate_recommendations(metrics)

        # Revenue breakdown chart
        revenue_chart = self.create_ascii_chart(
            "Revenue Breakdown",
            {
                "PPV Sales": metrics.ppv_sales,
                "Custom Videos": metrics.custom_videos,
                "Tributes": metrics.tributes
            }
        )

        # Format subscriber changes
        keysha_change_str = f"+{metrics.keysha_sub_change}" if metrics.keysha_sub_change >= 0 else str(metrics.keysha_sub_change)
        becky_change_str = f"+{metrics.becky_sub_change}" if metrics.becky_sub_change >= 0 else str(metrics.becky_sub_change)

        # Format revenue change
        revenue_trend = "up" if metrics.revenue_change_pct >= 0 else "down"
        mrr_trend = "up" if metrics.mrr_change_pct >= 0 else "down"

        report = f"""## 📊 WEEKLY ANALYTICS REPORT - {date_range}

### 💰 REVENUE
- **Total Revenue:** ${metrics.total_revenue:,.2f}
- **MRR:** ${metrics.mrr:,.2f} ({mrr_trend} {abs(metrics.mrr_change_pct):.1f}% from last week)
- **PPV Sales:** ${metrics.ppv_sales:,.2f}
- **Custom Videos:** ${metrics.custom_videos:,.2f}
- **Tributes:** ${metrics.tributes:,.2f}

{revenue_chart}

### 👥 SUBSCRIBERS
- **Mistress Keysha:** {metrics.mistress_keysha_subs} subs ({keysha_change_str} from last week)
- **Cum Slut Becky:** {metrics.cum_slut_becky_subs} subs ({becky_change_str} from last week)
- **New subs this week:** {metrics.new_subs}
- **Churn rate:** {metrics.churn_rate:.1f}%

### 📱 SOCIAL MEDIA
- **Twitter:** {metrics.twitter_followers:,} followers, {metrics.twitter_engagement_rate:.1f}% engagement rate
- **Instagram:** {metrics.instagram_followers:,} followers, {metrics.instagram_likes_per_post:,} likes per post
- **TikTok:** {metrics.tiktok_views:,} views, {metrics.tiktok_new_followers:,} new followers

### 🎯 TOP PERFORMERS
- **Best selling PPV:** {metrics.best_ppv_title} - ${metrics.best_ppv_revenue:,.2f}
- **Most engaged Twitter post:** {metrics.most_engaged_tweet}
- **Highest tribute:** ${metrics.highest_tribute:,.2f}

### 💡 RECOMMENDATIONS
"""

        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"

        report += f"\n---\n*Report generated by Analytics Oracle on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*\n"

        return report

    def save_report(self, report: str) -> str:
        """Save report to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"weekly-analytics-{timestamp}.md"
        filepath = os.path.join(self.reports_dir, filename)

        with open(filepath, "w") as f:
            f.write(report)

        print(f"Report saved to: {filepath}")
        return filepath

    def send_telegram_report(self, report: str) -> bool:
        """Send report via Telegram"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            print("Telegram credentials not configured. Skipping Telegram send.")
            return False

        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": report,
                "parse_mode": "Markdown"
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            print("Report sent to Telegram successfully!")
            return True

        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return False

    def run(self) -> None:
        """Main execution flow"""
        print("🔮 Analytics Oracle - Generating Weekly Report...")
        print("=" * 60)

        try:
            # Generate metrics
            metrics = self.generate_kpi_metrics()

            # Generate report
            report = self.generate_report(metrics)

            # Save report
            filepath = self.save_report(report)

            # Send to Telegram
            self.send_telegram_report(report)

            # Print to console
            print("\n" + report)

            print("\n" + "=" * 60)
            print("✅ Analytics Oracle completed successfully!")

        except Exception as e:
            print(f"❌ Error running Analytics Oracle: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Entry point"""
    oracle = AnalyticsOracle()
    oracle.run()


if __name__ == "__main__":
    main()
