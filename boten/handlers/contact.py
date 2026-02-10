"""
Contact command handler.

Displays contact information for support.
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.formatters import format_contact_info, format_schedule_info
from utils.keyboards import get_back_to_menu_keyboard
from utils.logger import setup_logger, log_command

logger = setup_logger("handlers.contact")


async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /contact command.

    Shows contact information and support hours.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/contact")

    contact_text = format_contact_info()
    schedule_text = format_schedule_info()

    keyboard = get_back_to_menu_keyboard()
    message_text = f"{contact_text}\n\n{schedule_text}"

    await update.message.reply_text(
        message_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    logger.info(f"Contact info displayed for user {user_id}")
