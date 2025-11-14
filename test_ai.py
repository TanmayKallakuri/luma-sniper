#!/usr/bin/env python3
"""
Test script to verify FriendliAI and Opik integration without Luma credentials.
"""

from friendli_client import FriendliClient
from opik_tracker import OpikTracker
from config import Config

# Sample test events
TEST_EVENTS = [
    {
        "title": "AI/ML Hackathon - Build with Claude & GPT-4",
        "description": "Join us for a 24-hour hackathon where you'll build innovative AI applications using the latest LLMs. Prizes for best projects! Focus on machine learning, natural language processing, and practical AI applications.",
        "url": "https://lu.ma/test-event-1",
        "date": "Nov 20, 2025",
        "location": "San Francisco, CA"
    },
    {
        "title": "Yoga and Meditation Retreat",
        "description": "Relax and rejuvenate with a weekend of yoga, meditation, and mindfulness. All levels welcome. Includes healthy meals and accommodation.",
        "url": "https://lu.ma/test-event-2",
        "date": "Nov 25, 2025",
        "location": "Marin County, CA"
    },
    {
        "title": "Web3 Developer Meetup - Smart Contracts & DeFi",
        "description": "Monthly meetup for blockchain developers. This month: Building secure smart contracts and exploring DeFi protocols. Network with other Web3 developers and share knowledge.",
        "url": "https://lu.ma/test-event-3",
        "date": "Nov 18, 2025",
        "location": "Virtual"
    },
    {
        "title": "Startup Founder Networking Night",
        "description": "Connect with fellow startup founders, investors, and entrepreneurs. Share experiences, discuss challenges, and make valuable connections in the startup ecosystem.",
        "url": "https://lu.ma/test-event-4",
        "date": "Nov 22, 2025",
        "location": "Palo Alto, CA"
    }
]

def main():
    print("🧪 Testing Luma Sniper Bot Components")
    print("=" * 60)

    # Initialize clients
    print("\n1️⃣ Initializing FriendliAI client...")
    ai_client = FriendliClient()
    print("   ✅ FriendliAI client initialized")

    print("\n2️⃣ Initializing Opik tracker...")
    tracker = OpikTracker()
    print("   ✅ Opik tracker initialized")

    # Start a test run
    print("\n3️⃣ Starting test tracking run...")
    tracker.start_run("test_run")

    print("\n4️⃣ Testing AI event analysis...")
    print(f"   User interests: {', '.join(Config.INTERESTS)}\n")

    for i, event in enumerate(TEST_EVENTS, 1):
        print(f"\n--- Test Event {i}/{len(TEST_EVENTS)} ---")
        print(f"📅 {event['title']}")

        # Log event discovery
        tracker.log_event_discovered(event)

        # Analyze with AI
        print(f"🤖 Analyzing event...")
        analysis = ai_client.analyze_event(event, Config.INTERESTS)

        # Log analysis
        tracker.log_event_analysis(event, analysis)

        # Display results
        print(f"   Score: {analysis['score']}/100")
        print(f"   Reasoning: {analysis['reasoning']}")
        print(f"   Decision: {'✅ WOULD REGISTER' if analysis['should_register'] else '❌ WOULD SKIP'}")

        # Simulate registration logging (without actual registration)
        if analysis['should_register']:
            tracker.log_registration_attempt(event, True, None)
            print(f"   📝 Logged as would-register event")

    # End tracking run
    print("\n5️⃣ Ending tracking run...")
    tracker.end_run()

    print("\n" + "=" * 60)
    print("✅ Test completed successfully!")
    print("\n📊 Next steps:")
    print("   1. Check your Opik dashboard for logged events")
    print("   2. Verify AI analysis makes sense for your interests")
    print("   3. When ready, add Luma credentials to .env")
    print("   4. Run: python bot.py --once")

if __name__ == "__main__":
    main()
