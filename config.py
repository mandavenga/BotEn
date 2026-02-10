"""
Configuration module for SpeakFlow English bot.

This module handles all environment variables, validation, and default values.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration class for the bot."""

    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "")

    # OpenRouter Configuration
    OPENROUTER_API_KEY: str = os.environ.get("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    OPENROUTER_BASE_URL: str = os.getenv(
        "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
    )

    # Bot Configuration
    BOT_NAME: str = os.getenv("BOT_NAME", "SpeakFlow English Support")
    MAX_HISTORY_MESSAGES: int = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))

    # AI Configuration
    AI_TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "1024"))
    AI_RETRY_ATTEMPTS: int = int(os.getenv("AI_RETRY_ATTEMPTS", "3"))
    AI_CACHE_TTL: int = int(os.getenv("AI_CACHE_TTL", "900"))  # 15 minutes

    # Feature Flags
    ENABLE_BOOKING: bool = os.getenv("ENABLE_BOOKING", "true").lower() == "true"
    ENABLE_AI_CHAT: bool = os.getenv("ENABLE_AI_CHAT", "true").lower() == "true"

    # Timeouts and Limits
    BOOKING_TIMEOUT_MINUTES: int = int(os.getenv("BOOKING_TIMEOUT_MINUTES", "10"))
    MAX_MESSAGE_LENGTH: int = 4096  # Telegram limit

    # Paths
    BASE_DIR: Path = Path(__file__).parent
    KNOWLEDGE_DIR: Path = BASE_DIR / "knowledge"
    ASSETS_DIR: Path = BASE_DIR / "assets"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")  # text or json

    @classmethod
    def validate(cls) -> None:
        """
        Validate required configuration values.

        Raises:
            ValueError: If required configuration is missing.
        """
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")

        if cls.MAX_HISTORY_MESSAGES < 1:
            raise ValueError("MAX_HISTORY_MESSAGES must be at least 1")

        if cls.AI_TEMPERATURE < 0 or cls.AI_TEMPERATURE > 2:
            raise ValueError("AI_TEMPERATURE must be between 0 and 2")

        if cls.AI_MAX_TOKENS < 1:
            raise ValueError("AI_MAX_TOKENS must be at least 1")

    @classmethod
    def get_knowledge_file(cls, filename: str) -> Optional[Path]:
        """
        Get path to a knowledge file.

        Args:
            filename: Name of the knowledge file (e.g., 'company.txt')

        Returns:
            Path object if file exists, None otherwise
        """
        path = cls.KNOWLEDGE_DIR / filename
        return path if path.exists() else None


# Validate configuration on import
Config.validate()
