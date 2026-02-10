"""
Reset command handler.

Clears conversation history and returns to main menu.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.conversation_manager import ConversationManager
from utils.keyboards import get_main_menu_keyboard
from utils.logger import setup_logger, log_command

logger = setup_logger("handlers.reset")


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /reset command.

    Clears conversation history and booking data, returns to main menu.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/reset")

    # Clear all user data
    ConversationManager.clear_history(context)
    ConversationManager.clear_booking_data(context)
    ConversationManager.reset_state(context)

    keyboard = get_main_menu_keyboard()
    message_text = (
        "🔄 История разговора очищена!\n\n"
        "Чем могу помочь?"
    )

    await update.message.reply_text(
        message_text,
        reply_markup=keyboard
    )

    logger.info(f"Conversation reset for user {user_id}")
