"""
Logging configuration for SpeakFlow English bot.

Provides structured logging with different formats and levels.
"""

import logging
import sys
from typing import Optional

from config import Config


def setup_logger(
    name: str = "speakflow_bot", level: Optional[str] = None
) -> logging.Logger:
    """
    Setup and configure logger for the bot.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    log_level = getattr(logging, level or Config.LOG_LEVEL)
    logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Choose format based on config
    if Config.LOG_FORMAT == "json":
        # JSON format for production
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def log_command(logger: logging.Logger, user_id: int, command: str) -> None:
    """
    Log a user command execution.

    Args:
        logger: Logger instance
        user_id: Telegram user ID
        command: Command name (e.g., '/start', '/help')
    """
    logger.info(f"User {user_id} executed command: {command}")


def log_error(logger: logging.Logger, error: Exception, context: str = "") -> None:
    """
    Log an error with context.

    Args:
        logger: Logger instance
        error: Exception object
        context: Additional context about where the error occurred
    """
    context_str = f" [{context}]" if context else ""
    logger.error(f"Error{context_str}: {type(error).__name__}: {str(error)}")


def log_ai_response(
    logger: logging.Logger, user_id: int, response_time: float, success: bool = True
) -> None:
    """
    Log AI response metrics.

    Args:
        logger: Logger instance
        user_id: Telegram user ID
        response_time: Time taken to get AI response (in seconds)
        success: Whether the AI call was successful
    """
    status = "success" if success else "failed"
    logger.info(
        f"AI response for user {user_id}: {status}, time: {response_time:.2f}s"
    )


# Create default logger instance
default_logger = setup_logger()
