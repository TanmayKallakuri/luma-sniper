#!/usr/bin/env python3
"""
Luma Event Sniper Bot

Automatically monitors Luma events and registers for events matching your interests
using FriendliAI for intelligent matching and Opik/Comet for experiment tracking.
"""

import time
import signal
import sys
from typing import List, Dict
from config import Config
from luma_scraper import LumaScraper
from friendli_client import FriendliClient
from opik_tracker import OpikTracker


class LumaSniperBot:
    """Main bot class that orchestrates event sniping."""

    def __init__(self):
        self.scraper = LumaScraper()
        self.ai_client = FriendliClient()
        self.tracker = OpikTracker()
        self.running = False

    def run_once(self) -> Dict:
        """
        Run a single iteration of the bot.

        Returns:
            Dictionary with run statistics
        """
        print("\n" + "=" * 60)
        print("🎯 Starting Luma Event Sniper Run")
        print("=" * 60)

        self.tracker.start_run()

        try:
            # Discover events
            print("\n📡 Discovering events...")
            events = self.scraper.discover_events()

            if not events:
                print("ℹ️  No new events found")
                return {"events_found": 0, "events_registered": 0}

            print(f"✅ Found {len(events)} new events\n")

            registered_count = 0

            # Process each event
            for i, event in enumerate(events, 1):
                print(f"\n--- Event {i}/{len(events)} ---")
                self.tracker.log_event_discovered(event)

                # Analyze event with AI
                print(f"🤖 Analyzing: {event['title']}")
                analysis = self.ai_client.analyze_event(event, Config.INTERESTS)

                self.tracker.log_event_analysis(event, analysis)

                print(f"   Score: {analysis['score']}/100")
                print(f"   Reasoning: {analysis['reasoning']}")
                print(f"   Decision: {'✅ REGISTER' if analysis['should_register'] else '❌ SKIP'}")

                # Register if AI recommends it
                if analysis["should_register"]:
                    print(f"\n🎯 Registering for event...")
                    success = self.scraper.register_for_event(event["url"])

                    self.tracker.log_registration_attempt(event, success)

                    if success:
                        registered_count += 1
                        print(f"✅ Successfully registered! ({registered_count} total)")
                    else:
                        print("❌ Registration failed")

                    # Rate limiting
                    time.sleep(2)
                else:
                    print("⏭️  Skipping event")

            return {"events_found": len(events), "events_registered": registered_count}

        except Exception as e:
            print(f"\n❌ Error during bot run: {e}")
            import traceback

            traceback.print_exc()
            return {"events_found": 0, "events_registered": 0, "error": str(e)}

        finally:
            self.tracker.end_run()
            print("\n" + "=" * 60)
            print("✅ Run completed")
            print("=" * 60)

    def run_continuous(self):
        """Run the bot continuously with scheduled intervals."""
        print("🚀 Starting Luma Sniper Bot in continuous mode")
        print(f"   Checking every {Config.CHECK_INTERVAL_MINUTES} minutes")
        print(f"   Interests: {', '.join(Config.INTERESTS)}")
        print("\n   Press Ctrl+C to stop\n")

        self.running = True

        # Setup signal handler for graceful shutdown
        def signal_handler(sig, frame):
            print("\n\n⚠️  Shutdown signal received")
            self.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            while self.running:
                self.run_once()

                if self.running:
                    wait_seconds = Config.CHECK_INTERVAL_MINUTES * 60
                    print(f"\n⏰ Waiting {Config.CHECK_INTERVAL_MINUTES} minutes until next check...")
                    time.sleep(wait_seconds)

        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            self.stop()

    def stop(self):
        """Stop the bot and clean up resources."""
        print("\n🛑 Stopping bot...")
        self.running = False
        self.scraper.close()
        print("✅ Bot stopped cleanly")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Luma Event Sniper Bot")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit (default: run continuously)",
    )
    parser.add_argument(
        "--test-config",
        action="store_true",
        help="Test configuration and exit",
    )

    args = parser.parse_args()

    # Validate configuration
    if not Config.validate():
        print("\n❌ Configuration validation failed!")
        print("   Please check your .env file and ensure all required fields are set.")
        print("   See .env.example for reference.")
        sys.exit(1)

    if args.test_config:
        print("✅ Configuration is valid!")
        print(f"\n📋 Settings:")
        print(f"   Interests: {', '.join(Config.INTERESTS)}")
        print(f"   Check interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
        print(f"   Max events per run: {Config.MAX_EVENTS_PER_RUN}")
        sys.exit(0)

    # Create and run bot
    bot = LumaSniperBot()

    try:
        if args.once:
            result = bot.run_once()
            print(f"\n📊 Final Stats:")
            print(f"   Events found: {result.get('events_found', 0)}")
            print(f"   Events registered: {result.get('events_registered', 0)}")
        else:
            bot.run_continuous()
    finally:
        bot.stop()


if __name__ == "__main__":
    main()
