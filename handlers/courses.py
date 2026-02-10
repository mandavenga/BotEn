"""
Courses command handler.

Displays course catalog with navigation.
"""

from telegram import Update
from telegram.ext import ContextTypes
from pathlib import Path

from config import Config
from utils.keyboards import get_courses_keyboard
from utils.logger import setup_logger, log_command

logger = setup_logger("handlers.courses")


async def courses_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /courses command.

    Shows course catalog with category navigation.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/courses")

    # Load courses overview
    courses_path = Config.get_knowledge_file("courses.txt")
    if courses_path:
        try:
            content = courses_path.read_text(encoding="utf-8")
            # Extract just the catalog section (first ~50 lines)
            lines = content.split('\n')
            overview = '\n'.join(lines[:50])
        except Exception as e:
            logger.error(f"Failed to load courses: {e}")
            overview = "Информация о курсах временно недоступна."
    else:
        overview = "Информация о курсах временно недоступна."

    keyboard = get_courses_keyboard()
    message_text = f"📚 <b>Каталог курсов SpeakFlow English</b>\n\n{overview}\n\nВыберите категорию для подробной информации:"

    await update.message.reply_text(
        message_text[:4000],  # Telegram limit
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    logger.info(f"Courses catalog displayed for user {user_id}")
