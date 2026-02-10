"""
Conversation history and state management.

Manages per-user conversation history and conversation state (normal, booking, etc).
"""

from typing import Dict, List, Optional
from enum import Enum
from telegram.ext import ContextTypes

from config import Config
from utils.logger import setup_logger

logger = setup_logger("conversation_manager")


class ConversationState(Enum):
    """Possible conversation states."""

    IDLE = "idle"
    BOOKING_COURSE = "booking_course"
    BOOKING_TIME = "booking_time"
    BOOKING_NAME = "booking_name"
    BOOKING_EMAIL = "booking_email"
    BOOKING_PHONE = "booking_phone"
    BOOKING_CONFIRM = "booking_confirm"
    AI_CHAT = "ai_chat"


class ConversationManager:
    """Manages conversation history and state for users."""

    @staticmethod
    def get_history(context: ContextTypes.DEFAULT_TYPE) -> List[Dict[str, str]]:
        """
        Get conversation history for the current user.

        Args:
            context: Telegram context object

        Returns:
            List of message dictionaries with 'role' and 'content'
        """
        if "history" not in context.user_data:
            context.user_data["history"] = []
        return context.user_data["history"]

    @staticmethod
    def add_message(
        context: ContextTypes.DEFAULT_TYPE, role: str, content: str
    ) -> None:
        """
        Add a message to conversation history.

        Args:
            context: Telegram context object
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        history = ConversationManager.get_history(context)
        history.append({"role": role, "content": content})

        # Trim history if too long
        max_messages = Config.MAX_HISTORY_MESSAGES * 2  # user + assistant pairs
        if len(history) > max_messages:
            context.user_data["history"] = history[-max_messages:]

    @staticmethod
    def clear_history(context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Clear conversation history.

        Args:
            context: Telegram context object
        """
        context.user_data["history"] = []
        logger.info("Conversation history cleared")

    @staticmethod
    def get_state(context: ContextTypes.DEFAULT_TYPE) -> ConversationState:
        """
        Get current conversation state.

        Args:
            context: Telegram context object

        Returns:
            Current conversation state
        """
        state = context.user_data.get("conversation_state", ConversationState.IDLE.value)
        try:
            return ConversationState(state)
        except ValueError:
            return ConversationState.IDLE

    @staticmethod
    def set_state(context: ContextTypes.DEFAULT_TYPE, state: ConversationState) -> None:
        """
        Set conversation state.

        Args:
            context: Telegram context object
            state: New conversation state
        """
        context.user_data["conversation_state"] = state.value
        logger.info(f"Conversation state changed to: {state.value}")

    @staticmethod
    def reset_state(context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Reset conversation state to IDLE.

        Args:
            context: Telegram context object
        """
        ConversationManager.set_state(context, ConversationState.IDLE)

    @staticmethod
    def is_in_booking_flow(context: ContextTypes.DEFAULT_TYPE) -> bool:
        """
        Check if user is in booking flow.

        Args:
            context: Telegram context object

        Returns:
            True if in any booking state
        """
        state = ConversationManager.get_state(context)
        return state in [
            ConversationState.BOOKING_COURSE,
            ConversationState.BOOKING_TIME,
            ConversationState.BOOKING_NAME,
            ConversationState.BOOKING_EMAIL,
            ConversationState.BOOKING_PHONE,
            ConversationState.BOOKING_CONFIRM,
        ]

    @staticmethod
    def get_user_data(context: ContextTypes.DEFAULT_TYPE, key: str) -> Optional[any]:
        """
        Get user data by key.

        Args:
            context: Telegram context object
            key: Data key

        Returns:
            User data value or None
        """
        return context.user_data.get(key)

    @staticmethod
    def set_user_data(context: ContextTypes.DEFAULT_TYPE, key: str, value: any) -> None:
        """
        Set user data.

        Args:
            context: Telegram context object
            key: Data key
            value: Data value
        """
        context.user_data[key] = value

    @staticmethod
    def clear_booking_data(context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Clear all booking-related data.

        Args:
            context: Telegram context object
        """
        booking_keys = [
            "booking_course",
            "booking_time",
            "booking_name",
            "booking_email",
            "booking_phone",
        ]

        for key in booking_keys:
            if key in context.user_data:
                del context.user_data[key]

        logger.info("Booking data cleared")
