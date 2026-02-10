"""
Help command handler.

Displays list of all available commands and their descriptions.
"""

from telegram import Update
from telegram.ext import ContextTypes

from utils.formatters import format_help_message
from utils.logger import setup_logger, log_command

logger = setup_logger("handlers.help")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command.

    Shows list of all available commands with descriptions.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/help")

    help_text = format_help_message()

    await update.message.reply_text(
        help_text,
        parse_mode="HTML"
    )

    logger.info(f"Help displayed for user {user_id}")
