"""
Reviews command handler.

Displays student testimonials and success stories.
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import Config
from utils.keyboards import get_back_to_menu_keyboard
from utils.logger import setup_logger, log_command
from utils.formatters import split_long_message

logger = setup_logger("handlers.reviews")


async def reviews_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /reviews command.

    Shows student testimonials and success stories.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/reviews")

    # Load testimonials
    testimonials_path = Config.get_knowledge_file("testimonials.txt")
    if testimonials_path:
        try:
            content = testimonials_path.read_text(encoding="utf-8")
            # Show first 2-3 reviews as overview
            lines = content.split('\n')
            overview = '\n'.join(lines[:180])
            overview += "\n\n💡 <i>Больше отзывов студентов на нашем сайте и в чате со мной!</i>"
        except Exception as e:
            logger.error(f"Failed to load reviews: {e}")
            overview = "Отзывы временно недоступны."
    else:
        overview = "Отзывы временно недоступны."

    keyboard = get_back_to_menu_keyboard()
    message_text = f"⭐ <b>Отзывы наших студентов</b>\n\n{overview}"

    # Split long message
    parts = split_long_message(message_text)
    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            # Last part with keyboard
            await update.message.reply_text(
                part,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(part, parse_mode="HTML")

    logger.info(f"Reviews displayed for user {user_id}")
