"""
Booking flow state machine and logic.

Manages the multi-step booking process for trial lessons.
"""

from typing import Optional, Dict
from telegram.ext import ContextTypes

from services.conversation_manager import ConversationManager, ConversationState
from utils.validators import validate_email, validate_phone, validate_name
from utils.logger import setup_logger

logger = setup_logger("booking_manager")


class BookingManager:
    """Manages booking flow state machine."""

    # Course name mappings for display
    COURSE_NAMES = {
        "book_a1a2": "General English A1-A2 (Beginner)",
        "book_b1b2": "General English B1-B2 (Intermediate)",
        "book_speaking": "Speaking Booster",
        "book_business": "Business English",
        "book_exam": "IELTS/TOEFL Preparation",
        "book_it": "IT English",
        "book_relocation": "English for Relocation",
    }

    # Time slot mappings for display
    TIME_SLOTS = {
        "time_morning": "Утро (08:00-09:00 МСК)",
        "time_afternoon": "День (13:00-14:00 МСК)",
        "time_evening": "Вечер (19:00-20:00 МСК)",
        "time_late": "Поздний вечер (20:30-21:30 МСК)",
    }

    @staticmethod
    def start_booking(context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Start the booking flow.

        Args:
            context: Telegram context object
        """
        ConversationManager.set_state(context, ConversationState.BOOKING_COURSE)
        ConversationManager.clear_booking_data(context)
        logger.info("Started booking flow")

    @staticmethod
    def cancel_booking(context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Cancel the booking flow and reset state.

        Args:
            context: Telegram context object
        """
        ConversationManager.clear_booking_data(context)
        ConversationManager.reset_state(context)
        logger.info("Booking cancelled")

    @staticmethod
    def set_course(context: ContextTypes.DEFAULT_TYPE, course_id: str) -> bool:
        """
        Set selected course and move to time selection.

        Args:
            context: Telegram context object
            course_id: Course identifier (e.g., 'book_a1a2')

        Returns:
            True if successful
        """
        if course_id in BookingManager.COURSE_NAMES:
            course_name = BookingManager.COURSE_NAMES[course_id]
            ConversationManager.set_user_data(context, "booking_course", course_name)
            ConversationManager.set_state(context, ConversationState.BOOKING_TIME)
            logger.info(f"Course selected: {course_name}")
            return True
        return False

    @staticmethod
    def set_time(context: ContextTypes.DEFAULT_TYPE, time_id: str) -> bool:
        """
        Set selected time slot and move to name input.

        Args:
            context: Telegram context object
            time_id: Time slot identifier (e.g., 'time_morning')

        Returns:
            True if successful
        """
        if time_id in BookingManager.TIME_SLOTS:
            time_slot = BookingManager.TIME_SLOTS[time_id]
            ConversationManager.set_user_data(context, "booking_time", time_slot)
            ConversationManager.set_state(context, ConversationState.BOOKING_NAME)
            logger.info(f"Time selected: {time_slot}")
            return True
        return False

    @staticmethod
    def set_name(context: ContextTypes.DEFAULT_TYPE, name: str) -> tuple[bool, str]:
        """
        Validate and set student name.

        Args:
            context: Telegram context object
            name: Student name

        Returns:
            Tuple of (success, error_message)
        """
        is_valid, error = validate_name(name)

        if is_valid:
            ConversationManager.set_user_data(context, "booking_name", name)
            ConversationManager.set_state(context, ConversationState.BOOKING_EMAIL)
            logger.info(f"Name set: {name}")
            return True, ""
        else:
            return False, error

    @staticmethod
    def set_email(context: ContextTypes.DEFAULT_TYPE, email: str) -> tuple[bool, str]:
        """
        Validate and set student email.

        Args:
            context: Telegram context object
            email: Student email

        Returns:
            Tuple of (success, error_message)
        """
        is_valid, error = validate_email(email)

        if is_valid:
            ConversationManager.set_user_data(context, "booking_email", email)
            ConversationManager.set_state(context, ConversationState.BOOKING_PHONE)
            logger.info(f"Email set: {email}")
            return True, ""
        else:
            return False, error

    @staticmethod
    def set_phone(
        context: ContextTypes.DEFAULT_TYPE, phone: str
    ) -> tuple[bool, str]:
        """
        Validate and set student phone (optional).

        Args:
            context: Telegram context object
            phone: Student phone number

        Returns:
            Tuple of (success, error_message)
        """
        # Phone is optional, allow skipping with empty string
        if not phone or phone.lower() in ["пропустить", "skip", "-"]:
            ConversationManager.set_user_data(context, "booking_phone", None)
            ConversationManager.set_state(context, ConversationState.BOOKING_CONFIRM)
            logger.info("Phone skipped")
            return True, ""

        is_valid, error = validate_phone(phone)

        if is_valid:
            ConversationManager.set_user_data(context, "booking_phone", phone)
            ConversationManager.set_state(context, ConversationState.BOOKING_CONFIRM)
            logger.info(f"Phone set: {phone}")
            return True, ""
        else:
            return False, error

    @staticmethod
    def get_booking_summary(context: ContextTypes.DEFAULT_TYPE) -> Optional[Dict[str, str]]:
        """
        Get summary of current booking data.

        Args:
            context: Telegram context object

        Returns:
            Dictionary with booking data or None if incomplete
        """
        booking_data = {
            "course": ConversationManager.get_user_data(context, "booking_course"),
            "time": ConversationManager.get_user_data(context, "booking_time"),
            "name": ConversationManager.get_user_data(context, "booking_name"),
            "email": ConversationManager.get_user_data(context, "booking_email"),
            "phone": ConversationManager.get_user_data(context, "booking_phone"),
        }

        # Check if required fields are present
        if not all([booking_data["course"], booking_data["time"],
                    booking_data["name"], booking_data["email"]]):
            return None

        return booking_data

    @staticmethod
    def confirm_booking(context: ContextTypes.DEFAULT_TYPE) -> bool:
        """
        Confirm the booking and reset state.

        Args:
            context: Telegram context object

        Returns:
            True if booking was confirmed successfully
        """
        booking_data = BookingManager.get_booking_summary(context)

        if booking_data:
            logger.info(f"Booking confirmed: {booking_data}")
            # In a real system, this would save to database, send emails, etc.

            # Clear booking data and reset state
            ConversationManager.clear_booking_data(context)
            ConversationManager.reset_state(context)
            return True

        return False

    @staticmethod
    def get_current_step_message(context: ContextTypes.DEFAULT_TYPE) -> str:
        """
        Get instruction message for current booking step.

        Args:
            context: Telegram context object

        Returns:
            Instruction message for current step
        """
        state = ConversationManager.get_state(context)

        messages = {
            ConversationState.BOOKING_COURSE: "Выберите интересующий вас курс:",
            ConversationState.BOOKING_TIME: "Выберите удобное время для занятий:",
            ConversationState.BOOKING_NAME: "Введите ваше имя:",
            ConversationState.BOOKING_EMAIL: "Введите ваш email:",
            ConversationState.BOOKING_PHONE: (
                "Введите ваш телефон (или напишите 'пропустить' если не хотите указывать):"
            ),
            ConversationState.BOOKING_CONFIRM: "Проверьте данные и подтвердите запись:",
        }

        return messages.get(state, "")
