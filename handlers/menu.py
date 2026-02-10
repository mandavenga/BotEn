"""
Menu command handler.

Returns user to main menu with inline keyboard.
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.keyboards import get_main_menu_keyboard
from utils.logger import setup_logger, log_command

logger = setup_logger("handlers.menu")


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /menu command.

    Displays main menu with inline keyboard.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/menu")

    keyboard = get_main_menu_keyboard()
    message_text = "📋 Главное меню SpeakFlow English\n\nВыберите интересующий раздел:"

    await update.message.reply_text(
        message_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    logger.info(f"Main menu displayed for user {user_id}")
