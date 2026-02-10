"""
FAQ command handler.

Displays frequently asked questions with categories.
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import Config
from utils.keyboards import get_faq_categories_keyboard
from utils.logger import setup_logger, log_command

logger = setup_logger("handlers.faq")


async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /faq command.

    Shows FAQ categories for navigation.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/faq")

    keyboard = get_faq_categories_keyboard()
    message_text = (
        "❓ <b>Часто задаваемые вопросы</b>\n\n"
        "Выберите категорию вопросов или спросите меня напрямую в чате!\n\n"
        "У нас есть ответы на вопросы о курсах, оплате, расписании, "
        "преподавателях, сертификатах и многом другом."
    )

    await update.message.reply_text(
        message_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    logger.info(f"FAQ categories displayed for user {user_id}")
