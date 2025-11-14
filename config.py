"""Configuration management for Luma Sniper Bot."""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for the Luma Sniper Bot."""

    # FriendliAI Configuration
    FRIENDLI_API_KEY = os.getenv("FRIENDLI_API_KEY")
    FRIENDLI_BASE_URL = os.getenv("FRIENDLI_BASE_URL", "https://api.friendli.ai/v1")

    # Opik Configuration
    OPIK_API_KEY = os.getenv("OPIK_API_KEY")
    OPIK_WORKSPACE = os.getenv("OPIK_WORKSPACE")

    # Luma Credentials
    LUMA_EMAIL = os.getenv("LUMA_EMAIL")
    LUMA_PASSWORD = os.getenv("LUMA_PASSWORD")

    # Bot Configuration
    CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "15"))
    MAX_EVENTS_PER_RUN = int(os.getenv("MAX_EVENTS_PER_RUN", "10"))

    # User Interests
    INTERESTS: List[str] = os.getenv("INTERESTS", "").split(",")
    INTERESTS = [interest.strip() for interest in INTERESTS if interest.strip()]

    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present."""
        required_fields = [
            ("FRIENDLI_API_KEY", cls.FRIENDLI_API_KEY),
            ("OPIK_API_KEY", cls.OPIK_API_KEY),
            ("LUMA_EMAIL", cls.LUMA_EMAIL),
            ("LUMA_PASSWORD", cls.LUMA_PASSWORD),
        ]

        missing_fields = [field for field, value in required_fields if not value]

        if missing_fields:
            print(f"❌ Missing required configuration: {', '.join(missing_fields)}")
            return False

        if not cls.INTERESTS:
            print("⚠️  Warning: No interests configured. Bot may register for all events!")

        return True
