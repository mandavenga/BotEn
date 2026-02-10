"""
Prices command handler.

Displays pricing information and current promotions.
"""

from telegram import Update
from telegram.ext import ContextTypes

from config import Config
from utils.keyboards import get_back_to_menu_keyboard
from utils.logger import setup_logger, log_command

logger = setup_logger("handlers.prices")


async def prices_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /prices command.

    Shows pricing table and current promotions.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    log_command(logger, user_id, "/prices")

    # Load pricing information
    pricing_path = Config.get_knowledge_file("pricing.txt")
    if pricing_path:
        try:
            content = pricing_path.read_text(encoding="utf-8")
            # Extract main pricing section (first ~100 lines)
            lines = content.split('\n')
            pricing_info = '\n'.join(lines[:100])
        except Exception as e:
            logger.error(f"Failed to load pricing: {e}")
            pricing_info = "Информация о ценах временно недоступна."
    else:
        pricing_info = "Информация о ценах временно недоступна."

    keyboard = get_back_to_menu_keyboard()
    message_text = f"💰 <b>Цены и тарифы</b>\n\n{pricing_info}"

    # Split if too long
    if len(message_text) > 4000:
        parts = [message_text[i:i+4000] for i in range(0, len(message_text), 4000)]
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
    else:
        await update.message.reply_text(
            message_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    logger.info(f"Prices displayed for user {user_id}")
