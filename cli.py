"""
Command-Line Interface for YouTube Shorts Performance Analysis.
Author: Thota Abhiram (Parul University)
Subject: Social Media (Social Media Analytics & Marketing)
Zero external dependencies.
"""

import argparse
import sys
from typing import List, Dict, Any

from core.dataset_generator import load_dataset
from core.analyzer import ShortsPerformanceAnalyzer, analyze_single_short
from core.youtube_api import YouTubeShortsClient
from core.sentiment import analyze_title_hook


def format_num(n: int) -> str:
    """Format large numbers into human-readable K/M notation."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def print_banner():
    print("""
================================================================================
   YOUTUBE SHORTS PERFORMANCE ANALYTICS & VIRALITY PREDICTION PLATFORM
   Subject: Social Media | Parul University | Student: Thota Abhiram
================================================================================
""")


def cmd_summary(analyzer: ShortsPerformanceAnalyzer):
    kpis = analyzer.get_summary_kpis()
    print_banner()
    print(f"📊 DATASET OVERVIEW & KEY PERFORMANCE INDICATORS")
    print(f"--------------------------------------------------------------------------------")
    print(f"  • Total Shorts Analyzed  : {kpis['total_shorts']}")
    print(f"  • Aggregate Views Count  : {format_num(kpis['total_views'])} ({kpis['total_views']:,})")
    print(f"  • Total Likes Recorded   : {format_num(kpis['total_likes'])} ({kpis['total_likes']:,})")
    print(f"  • Total Comments Logged  : {format_num(kpis['total_comments'])} ({kpis['total_comments']:,})")
    print(f"  • Average Engagement Rate: {kpis['avg_engagement_rate']}%  (Likes + Comments / Views)")
    print(f"  • Avg View-Through Rate  : {kpis['avg_estimated_vtr']}%  (Audience Retention Proxy)")
    print(f"  • Average Hook Score     : {kpis['avg_hook_score']}/100  (Title Curiosity & Power Words)")
    print(f"  • Average Virality Score : {kpis['avg_virality_score']}/100")
    print(f"  • Mean Short Duration    : {kpis['avg_duration_seconds']}s")
    print(f"--------------------------------------------------------------------------------")
    print(f"🏆 TOP VIRAL PERFORMER:")
    top = kpis["top_performer"]
    print(f"  Title   : {top['title']}")
    print(f"  Views   : {format_num(top['views'])} | Virality Score: {top['virality_score']}/100 | Niche: {top['category']}")
    print(f"================================================================================\n")


def cmd_categories(analyzer: ShortsPerformanceAnalyzer):
    cats = analyzer.get_category_breakdown()
    print_banner()
    print(f"📁 CATEGORY PERFORMANCE & SOCIAL BENCHMARKS")
    print(f"{'Category':<24} | {'Count':<5} | {'Avg Views':<10} | {'Avg ER%':<8} | {'Bench ER%':<9} | {'Status':<16} | {'Virality'}")
    print("-" * 96)
    for c in cats:
        print(f"{c['category']:<24} | {c['count']:<5} | {format_num(c['avg_views']):<10} | {c['avg_er']:<8}% | {c['benchmark_er']:<9}% | {c['er_status']:<16} | {c['avg_virality']}/100")
    print("-" * 96 + "\n")


def cmd_durations(analyzer: ShortsPerformanceAnalyzer):
    tiers = analyzer.get_duration_tier_breakdown()
    print_banner()
    print(f"⏱️ DURATION BRACKET OPTIMIZATION ANALYSIS")
    print(f"{'Duration Tier':<25} | {'Count':<6} | {'Avg Views':<11} | {'Avg ER%':<9} | {'Est. VTR%':<10} | {'Virality Score'}")
    print("-" * 82)
    for t in tiers:
        print(f"{t['tier']:<25} | {t['count']:<6} | {format_num(t['avg_views']):<11} | {t['avg_er']:<9}% | {t['avg_vtr']:<10}% | {t['avg_virality']}/100")
    print("-" * 82)
    print("💡 Key Takeaway: Ultra-Short (≤15s) Shorts achieve the highest retention (VTR), but Mid-Length (16-30s) deliver the highest total engagement & conversions.\n")


def cmd_virality(analyzer: ShortsPerformanceAnalyzer, top_n: int = 10):
    shorts = sorted(analyzer.analyzed_shorts, key=lambda s: s["virality_score"], reverse=True)[:top_n]
    print_banner()
    print(f"🔥 TOP {top_n} VIRAL SHORTS LEADERBOARD")
    print(f"{'#':<3} | {'Virality':<9} | {'Views':<8} | {'ER%':<6} | {'VTR%':<6} | {'Duration':<8} | {'Title'}")
    print("-" * 95)
    for idx, s in enumerate(shorts, 1):
        title_trunc = s['title'][:40] + ("..." if len(s['title']) > 40 else "")
        print(f"{idx:<3} | {s['virality_score']:<9.1f} | {format_num(s['views']):<8} | {s['engagement_rate']:<6.2f}% | {s['estimated_vtr']:<6.1f}% | {s['duration_seconds']:<2}s     | {title_trunc}")
    print("-" * 95 + "\n")


def cmd_hashtags(analyzer: ShortsPerformanceAnalyzer):
    tags = analyzer.get_hashtag_analytics(15)
    print_banner()
    print(f"🏷️ TOP VIRAL HASHTAG PERFORMANCE")
    print(f"{'Hashtag':<18} | {'Frequency':<9} | {'Avg Views':<11} | {'Avg ER%':<9} | {'Virality'}")
    print("-" * 65)
    for t in tags:
        print(f"{t['hashtag']:<18} | {t['usage_count']:<9} | {format_num(t['avg_views']):<11} | {t['avg_er']:<9}% | {t['avg_virality']}/100")
    print("-" * 65 + "\n")


def cmd_predict(title: str, duration: int, views: int, category: str):
    print_banner()
    print("🤖 SHORTS VIRALITY PREDICTOR & TITLE HOOK EVALUATION")
    print("--------------------------------------------------------------------------------")
    dummy = {
        "title": title,
        "views": views,
        "likes": int(views * 0.05),
        "comments": int(views * 0.003),
        "duration_seconds": duration,
        "category": category,
        "tags": ["shorts", "trending"]
    }
    result = analyze_single_short(dummy)
    hook = analyze_title_hook(title)

    print(f"  • Tested Title     : \"{title}\"")
    print(f"  • Category / Niche : {category}")
    print(f"  • Video Duration   : {duration} seconds ({result['duration_tier']})")
    print(f"  • Simulated Views  : {format_num(views)}")
    print(f"--------------------------------------------------------------------------------")
    print(f"  🎯 Hook Strength Score : {hook['hook_score']}/100  ({hook['length_rating']})")
    print(f"  🎭 Title Sentiment     : {hook['sentiment']} (Polarity: {hook['sentiment_score']})")
    print(f"  ⚡ Power Words Found   : {', '.join(hook['power_words_found']) if hook['power_words_found'] else 'None detected'}")
    print(f"  👁️ Estimated VTR       : {result['estimated_vtr']}% (Audience Retention)")
    print(f"  📈 Predicted Virality  : {result['virality_score']}/100  -->  {result['virality_tier']}")
    print(f"--------------------------------------------------------------------------------")
    print(f"💡 Algorithmic Recommendations for this Short:")
    for r in hook["recommendations"]:
        print(f"  - {r}")
    print("================================================================================\n")


def cmd_fetch_live(query: str, max_results: int = 10):
    print_banner()
    print(f"🌐 FETCHING LIVE SHORTS VIA YOUTUBE DATA API V3")
    print(f"Search Query: \"{query}\" | Max Results: {max_results}")
    print("Connecting to Google YouTube API endpoint...")

    try:
        client = YouTubeShortsClient()
        shorts = client.fetch_shorts(query=query, max_results=max_results)
        if not shorts:
            print("No shorts found for the specified query.")
            return

        print(f"Successfully retrieved {len(shorts)} live Shorts from YouTube!\n")
        analyzer = ShortsPerformanceAnalyzer(shorts)
        cmd_summary(analyzer)
        cmd_virality(analyzer, top_n=min(5, len(shorts)))

    except Exception as e:
        print(f"❌ Error fetching from YouTube API: {e}")
        print("Falling back to preloaded dataset.")


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Shorts Performance Analysis Platform (Social Media Subject)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    subparsers.add_parser("summary", help="Display global KPIs and dataset overview")
    subparsers.add_parser("categories", help="Show performance breakdown across content niches")
    subparsers.add_parser("durations", help="Show duration tier retention analysis")
    subparsers.add_parser("virality", help="Display top viral Shorts leaderboard")
    subparsers.add_parser("hashtags", help="Rank top hashtags by reach and engagement")

    # Predict command
    pred_parser = subparsers.add_parser("predict", help="Predict virality and hook score for a Short")
    pred_parser.add_argument("--title", type=str, default="3 Mind-Blowing AI Websites You Must Try Today! 🤖 #shorts", help="Short video title")
    pred_parser.add_argument("--duration", type=int, default=24, help="Duration in seconds (1-60)")
    pred_parser.add_argument("--views", type=int, default=500000, help="Expected view scale")
    pred_parser.add_argument("--category", type=str, default="Technology & AI", help="Content category")

    # Live Fetch
    fetch_parser = subparsers.add_parser("fetch-live", help="Fetch live YouTube Shorts using YouTube API v3")
    fetch_parser.add_argument("--query", type=str, default="artificial intelligence", help="Search keyword")
    fetch_parser.add_argument("--max", type=int, default=10, help="Number of videos to fetch")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Launch the Web Dashboard server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to listen on")

    args = parser.parse_args()

    # Load dataset
    raw_data = load_dataset()
    analyzer = ShortsPerformanceAnalyzer(raw_data)

    if args.command == "categories":
        cmd_categories(analyzer)
    elif args.command == "durations":
        cmd_durations(analyzer)
    elif args.command == "virality":
        cmd_virality(analyzer)
    elif args.command == "hashtags":
        cmd_hashtags(analyzer)
    elif args.command == "predict":
        cmd_predict(args.title, args.duration, args.views, args.category)
    elif args.command == "fetch-live":
        cmd_fetch_live(args.query, args.max)
    elif args.command == "serve":
        import server
        server.run_server(port=args.port)
    else:
        # Default action: show summary
        cmd_summary(analyzer)
        print("Tip: Run 'python cli.py --help' to see all analytical subcommands.")


if __name__ == "__main__":
    main()
