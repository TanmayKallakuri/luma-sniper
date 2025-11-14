"""FriendliAI client for intelligent event matching."""
import requests
from typing import Dict, List
from config import Config


class FriendliClient:
    """Client for interacting with FriendliAI API."""

    def __init__(self):
        self.api_key = Config.FRIENDLI_API_KEY
        self.base_url = Config.FRIENDLI_BASE_URL
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
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "meta-llama-3.1-8b-instruct",  # Using efficient model
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

            # Parse the AI response
            return self._parse_ai_response(ai_response, event_data)

        except Exception as e:
            print(f"❌ Error analyzing event with FriendliAI: {e}")
            return {"score": 0, "reasoning": f"Analysis failed: {str(e)}", "should_register": False}

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

        # Fallback: basic keyword matching
        return self._fallback_analysis(event_data)

    def _fallback_analysis(self, event_data: Dict) -> Dict:
        """Fallback analysis if AI parsing fails."""
        title = event_data.get("title", "").lower()
        description = event_data.get("description", "").lower()
        text = f"{title} {description}"

        matches = sum(1 for interest in Config.INTERESTS if interest.lower() in text)
        score = min(matches * 25, 100)

        return {
            "score": score,
            "reasoning": f"Keyword match: {matches} interests found",
            "should_register": score >= 60,
        }
