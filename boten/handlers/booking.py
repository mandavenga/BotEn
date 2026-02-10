"""
Booking handler for multi-step trial lesson booking.

Manages the booking flow state machine.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.booking_manager import BookingManager
from services.conversation_manager import ConversationManager, ConversationState
from utils.keyboards import (
    get_booking_courses_keyboard,
    get_booking_time_keyboard,
    get_cancel_keyboard,
    get_back_to_menu_keyboard,
)
from utils.formatters import format_booking_confirmation
from utils.logger import setup_logger, log_command

logger = setup_logger("handlers.booking")


async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /book command.

    Starts the booking flow.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/book")

    # Start booking flow
    BookingManager.start_booking(context)

    keyboard = get_booking_courses_keyboard()
    message_text = (
        "📝 <b>Запись на пробное занятие</b>\n\n"
        "Отлично! Давайте запишем вас на бесплатный пробный урок (60 минут).\n\n"
        "Шаг 1/5: Выберите курс, который вас интересует:"
    )

    await update.message.reply_text(
        message_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    logger.info(f"Booking flow started for user {user_id}")


async def handle_booking_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle text input during booking flow.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    state = ConversationManager.get_state(context)
    user_input = update.message.text

    if state == ConversationState.BOOKING_NAME:
        # Validate and set name
        success, error = BookingManager.set_name(context, user_input)

        if success:
            message_text = (
                "✅ Отлично!\n\n"
                "Шаг 3/5: Введите ваш email для отправки подтверждения:"
            )
            keyboard = get_cancel_keyboard()
            await update.message.reply_text(
                message_text,
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text(
                f"⚠️ {error}\n\nПожалуйста, введите корректное имя:"
            )

    elif state == ConversationState.BOOKING_EMAIL:
        # Validate and set email
        success, error = BookingManager.set_email(context, user_input)

        if success:
            message_text = (
                "✅ Отлично!\n\n"
                "Шаг 4/5: Введите ваш телефон (или напишите 'пропустить'):"
            )
            keyboard = get_cancel_keyboard()
            await update.message.reply_text(
                message_text,
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text(
                f"⚠️ {error}\n\nПожалуйста, введите корректный email:"
            )

    elif state == ConversationState.BOOKING_PHONE:
        # Validate and set phone
        success, error = BookingManager.set_phone(context, user_input)

        if success:
            # Show confirmation
            booking_data = BookingManager.get_booking_summary(context)
            if booking_data:
                confirmation_text = format_booking_confirmation(
                    name=booking_data["name"],
                    course=booking_data["course"],
                    time=booking_data["time"],
                    email=booking_data["email"],
                    phone=booking_data.get("phone")
                )

                # Confirm booking
                BookingManager.confirm_booking(context)

                keyboard = get_back_to_menu_keyboard()
                await update.message.reply_text(
                    confirmation_text,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )

                logger.info(f"Booking completed for user {update.effective_user.id}")
            else:
                await update.message.reply_text(
                    "❌ Ошибка при обработке бронирования. Попробуйте снова /book"
                )
        else:
            await update.message.reply_text(
                f"⚠️ {error}\n\nПожалуйста, введите корректный телефон или 'пропустить':"
            )
