"""
Conversation handler for AI chat.

Handles free-form messages from users and generates AI responses.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.ai_service import AIService
from services.conversation_manager import ConversationManager
from utils.logger import setup_logger, log_error
from utils.formatters import split_long_message

logger = setup_logger("handlers.conversation")

# Initialize AI service
ai_service = AIService()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle regular text messages with AI.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    user_message = update.message.text

    if not user_message:
        return

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        # Add user message to history
        ConversationManager.add_message(context, "user", user_message)

        # Get conversation history
        history = ConversationManager.get_history(context)

        # Get AI response
        ai_response = ai_service.get_response(
            messages=history,
            user_id=user_id,
            context="general",
            use_cache=True
        )

        # Add AI response to history
        ConversationManager.add_message(context, "assistant", ai_response)

        # Send response (split if too long)
        parts = split_long_message(ai_response)
        for part in parts:
            await update.message.reply_text(part)

        logger.info(f"AI response sent to user {user_id}")

    except Exception as e:
        log_error(logger, e, "AI conversation")
        error_message = (
            "😔 Извините, произошла ошибка при обработке вашего сообщения. "
            "Пожалуйста, попробуйте позже или свяжитесь с поддержкой:\n\n"
            "📧 support@speakflow-english.com\n"
            "📱 +7 495 123 45 67"
        )
        await update.message.reply_text(error_message)
