"""
Start command handler.

Displays welcome message and main menu when user starts the bot.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.conversation_manager import ConversationManager
from utils.formatters import format_welcome_message
from utils.keyboards import get_main_menu_keyboard
from utils.logger import setup_logger, log_command

logger = setup_logger("handlers.start")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command.

    Clears conversation history and shows welcome message with main menu.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/start")

    # Clear conversation history
    ConversationManager.clear_history(context)
    ConversationManager.reset_state(context)

    # Send welcome message with main menu
    welcome_text = format_welcome_message()
    keyboard = get_main_menu_keyboard()

    await update.message.reply_text(
        welcome_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    logger.info(f"User {user_id} started the bot")
