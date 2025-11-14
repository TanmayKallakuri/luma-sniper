"""FriendliAI client for intelligent event matching."""
from typing import Dict, List
from config import Config


class FriendliClient:
    """Client for interacting with FriendliAI API."""

    def __init__(self):
        self.api_key = Config.FRIENDLI_API_KEY
        self.base_url = Config.FRIENDLI_BASE_URL
        self.use_openai_sdk = True  # Use OpenAI SDK for better compatibility

        if self.use_openai_sdk:
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                )
                print("✅ FriendliAI client initialized (using OpenAI SDK)")
            except ImportError:
                print("⚠️  OpenAI SDK not available, falling back to requests")
                self.use_openai_sdk = False
                import requests
                self.client = requests.Session()
                self.headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

    def analyze_event(self, event_data: Dict, user_interests: List[str]) -> Dict:
        """
        Analyze an event against user interests using FriendliAI.

        Args:
            event_data: Dictionary containing event information
            user_interests: List of user's interests

        Returns:
            Dictionary with relevance score and reasoning
        """
        prompt = self._build_analysis_prompt(event_data, user_interests)

        try:
            if self.use_openai_sdk:
                return self._analyze_with_openai_sdk(prompt, event_data)
            else:
                return self._analyze_with_requests(prompt, event_data)

        except Exception as e:
            print(f"❌ Error analyzing event with FriendliAI: {e}")
            print(f"   Falling back to keyword matching...")
            return self._fallback_analysis(event_data)

    def _analyze_with_openai_sdk(self, prompt: str, event_data: Dict) -> Dict:
        """Analyze using OpenAI SDK (recommended)."""
        response = self.client.chat.completions.create(
            model="meta-llama-3.1-8b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert event analyst. Analyze events and provide relevance scores based on user interests. Always respond in JSON format.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=300,
        )

        ai_response = response.choices[0].message.content
        return self._parse_ai_response(ai_response, event_data)

    def _analyze_with_requests(self, prompt: str, event_data: Dict) -> Dict:
        """Analyze using requests library (fallback)."""
        import requests

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json={
                "model": "meta-llama-3.1-8b-instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert event analyst. Analyze events and provide relevance scores based on user interests. Always respond in JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 300,
            },
            timeout=30,
        )
        response.raise_for_status()

        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        return self._parse_ai_response(ai_response, event_data)

    def _build_analysis_prompt(self, event_data: Dict, user_interests: List[str]) -> str:
        """Build the prompt for event analysis."""
        interests_str = ", ".join(user_interests)

        return f"""Analyze this event and determine if it matches the user's interests.

Event Details:
- Title: {event_data.get('title', 'N/A')}
- Description: {event_data.get('description', 'N/A')}
- Location: {event_data.get('location', 'N/A')}
- Date: {event_data.get('date', 'N/A')}

User Interests: {interests_str}

Provide your analysis in the following JSON format:
{{
    "score": <number from 0-100 indicating relevance>,
    "reasoning": "<brief explanation of why this event matches or doesn't match>",
    "should_register": <true or false>
}}

Score guidelines:
- 80-100: Highly relevant, definitely register
- 60-79: Moderately relevant, probably register
- 40-59: Somewhat relevant, maybe register
- 0-39: Not relevant, don't register

Respond ONLY with the JSON object, no additional text."""

    def _parse_ai_response(self, ai_response: str, event_data: Dict) -> Dict:
        """Parse the AI response and extract structured data."""
        import json
        import re

        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{[^{}]*"score"[^{}]*\}', ai_response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                return {
                    "score": parsed.get("score", 0),
                    "reasoning": parsed.get("reasoning", "No reasoning provided"),
                    "should_register": parsed.get("should_register", parsed.get("score", 0) >= 60),
                }
        except Exception as e:
            print(f"⚠️  Failed to parse AI response: {e}")
            print(f"   Response was: {ai_response[:200]}...")

        # Fallback: basic keyword matching
        print(f"   Using fallback keyword analysis")
        return self._fallback_analysis(event_data)

    def _fallback_analysis(self, event_data: Dict) -> Dict:
        """Fallback analysis if AI parsing fails or API is unavailable."""
        title = event_data.get("title", "").lower()
        description = event_data.get("description", "").lower()
        text = f"{title} {description}"

        matches = sum(1 for interest in Config.INTERESTS if interest.lower() in text)
        score = min(matches * 25, 100)

        return {
            "score": score,
            "reasoning": f"Keyword match: {matches} interests found ({', '.join([i for i in Config.INTERESTS if i.lower() in text])})" if matches > 0 else "No keyword matches found",
            "should_register": score >= 60,
        }
