"""
Teachers command handler.

Displays information about teaching team.
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import Config
from utils.keyboards import get_back_to_menu_keyboard
from utils.logger import setup_logger, log_command
from utils.formatters import split_long_message

logger = setup_logger("handlers.teachers")


async def teachers_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /teachers command.

    Shows teacher biographies and qualifications.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/teachers")

    # Load teachers information
    teachers_path = Config.get_knowledge_file("teachers.txt")
    if teachers_path:
        try:
            content = teachers_path.read_text(encoding="utf-8")
            # Show first 2-3 teachers as overview
            lines = content.split('\n')
            overview = '\n'.join(lines[:150])
            overview += "\n\n💡 <i>Полная информация о всех преподавателях доступна на сайте или спросите у меня в чате!</i>"
        except Exception as e:
            logger.error(f"Failed to load teachers: {e}")
            overview = "Информация о преподавателях временно недоступна."
    else:
        overview = "Информация о преподавателях временно недоступна."

    keyboard = get_back_to_menu_keyboard()
    message_text = f"👨‍🏫 <b>Наша команда преподавателей</b>\n\n{overview}"

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

    logger.info(f"Teachers info displayed for user {user_id}")
