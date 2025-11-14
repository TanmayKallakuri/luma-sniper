#!/usr/bin/env python3
"""
Quick test script to verify API keys work correctly.
Run this in VS Code to test your FriendliAI and Opik setup.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Test 1: Check environment variables
print("=" * 60)
print("🔍 API Key Configuration Test")
print("=" * 60)

friendli_key = os.getenv("FRIENDLI_API_KEY", "")
opik_key = os.getenv("OPIK_API_KEY", "")

print(f"\n1️⃣ FriendliAI API Key: {'✅ Set' if friendli_key else '❌ Not set'}")
if friendli_key:
    print(f"   Preview: {friendli_key[:10]}...{friendli_key[-10:]}")

print(f"\n2️⃣ Opik API Key: {'✅ Set' if opik_key else '❌ Not set'}")
if opik_key:
    print(f"   Preview: {opik_key[:10]}...{opik_key[-10:]}")

# Test 2: Try FriendliAI API
print("\n" + "=" * 60)
print("🤖 Testing FriendliAI API")
print("=" * 60)

if friendli_key:
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=friendli_key,
            base_url="https://api.friendli.ai/serverless/v1",
        )

        print("\n✅ OpenAI client initialized")
        print("📡 Sending test request...")

        response = client.chat.completions.create(
            model="meta-llama-3.1-8b-instruct",
            messages=[
                {"role": "user", "content": "Say 'API works!' and nothing else"}
            ],
            max_tokens=10,
        )

        result = response.choices[0].message.content
        print(f"✅ FriendliAI Response: {result}")
        print("🎉 FriendliAI API is working correctly!")

    except Exception as e:
        print(f"❌ FriendliAI API Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Verify your API key at https://suite.friendli.ai/")
        print("   2. Check if you have credits remaining")
        print("   3. Ensure the key has proper permissions")
else:
    print("⚠️  Skipping (no API key set)")

# Test 3: Try Opik
print("\n" + "=" * 60)
print("📊 Testing Opik/Comet API")
print("=" * 60)

if opik_key:
    try:
        import opik

        # Configure with workspace if available
        opik_workspace = os.getenv("OPIK_WORKSPACE", "")
        config_params = {"api_key": opik_key}
        if opik_workspace:
            config_params["workspace"] = opik_workspace
            print(f"   Using workspace: {opik_workspace}")

        opik.configure(**config_params)
        print("✅ Opik configured")

        # Try to create a simple trace using the client
        client = opik.Opik()
        trace = client.trace(
            name="test_trace",
            input={"test": "data"},
            output={"status": "success"},
        )
        trace.end()

        print("✅ Opik API is working correctly!")
        print("🎉 Check your Opik dashboard to see the test trace!")

    except Exception as e:
        print(f"❌ Opik API Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Verify your API key in Comet/Opik dashboard")
        print("   2. Check if the key has write permissions")
        print("   3. Ensure you're using the correct workspace")
else:
    print("⚠️  Skipping (no API key set)")

# Test 4: Event analysis simulation
print("\n" + "=" * 60)
print("🎯 Event Analysis Simulation")
print("=" * 60)

test_event = {
    "title": "AI/ML Hackathon - Build with LLMs",
    "description": "Join us for a 24-hour hackathon focused on AI and machine learning",
    "url": "https://example.com/event",
    "date": "Nov 20, 2025",
    "location": "San Francisco"
}

interests = ["AI", "Machine Learning", "Hackathons"]

if friendli_key:
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=friendli_key,
            base_url="https://api.friendli.ai/serverless/v1",
        )

        prompt = f"""Analyze this event and rate its relevance to these interests: {', '.join(interests)}

Event: {test_event['title']}
Description: {test_event['description']}

Respond with a JSON object: {{"score": <0-100>, "reasoning": "<brief explanation>"}}"""

        print(f"\n📅 Event: {test_event['title']}")
        print(f"🎯 Interests: {', '.join(interests)}")
        print("\n🤖 Asking AI to analyze...")

        response = client.chat.completions.create(
            model="meta-llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": "You are an event analyst. Respond only with JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150,
        )

        ai_response = response.choices[0].message.content
        print(f"\n✅ AI Analysis:\n{ai_response}")

    except Exception as e:
        print(f"❌ Error: {e}")
else:
    # Fallback keyword matching
    print(f"\n📅 Event: {test_event['title']}")
    print(f"🎯 Interests: {', '.join(interests)}")
    print("\n🔍 Using keyword matching (no AI key)...")

    text = f"{test_event['title']} {test_event['description']}".lower()
    matches = [i for i in interests if i.lower() in text]
    score = min(len(matches) * 25, 100)

    print(f"✅ Score: {score}/100")
    print(f"   Matches: {', '.join(matches) if matches else 'None'}")
    print(f"   Decision: {'REGISTER' if score >= 60 else 'SKIP'}")

print("\n" + "=" * 60)
print("✅ Test Complete!")
print("=" * 60)

print("\n📋 Next Steps:")
print("   1. If APIs work → Run: python bot.py --once")
print("   2. Add Luma credentials to .env for full registration")
print("   3. Customize INTERESTS in .env to your preferences")
print("\n🚀 Ready for your hackathon demo!")
