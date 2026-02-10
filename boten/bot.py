"""
Main bot application for SpeakFlow English.

Coordinates all modules and handles bot lifecycle.
"""

import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import Config
from utils.logger import setup_logger

# Import all command handlers
from handlers.start import start_command
from handlers.help import help_command
from handlers.menu import menu_command
from handlers.reset import reset_command
from handlers.courses import courses_command
from handlers.prices import prices_command
from handlers.teachers import teachers_command
from handlers.reviews import reviews_command
from handlers.faq import faq_command
from handlers.contact import contact_command
from handlers.booking import book_command, handle_booking_input
from handlers.conversation import handle_message
from handlers.callbacks import button_callback

# Import services
from services.conversation_manager import ConversationManager

logger = setup_logger("bot.main")


def main() -> None:
    """
    Main entry point for the bot.

    Initializes the application, registers handlers, and starts polling.
    """
    try:
        # Validate configuration
        Config.validate()

        logger.info("=" * 50)
        logger.info("SpeakFlow English Bot Starting")
        logger.info(f"Model: {Config.OPENROUTER_MODEL}")
        logger.info(f"AI Chat: {'Enabled' if Config.ENABLE_AI_CHAT else 'Disabled'}")
        logger.info(f"Booking: {'Enabled' if Config.ENABLE_BOOKING else 'Disabled'}")
        logger.info("=" * 50)

        # Create application
        app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

        # Register command handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("menu", menu_command))
        app.add_handler(CommandHandler("reset", reset_command))
        app.add_handler(CommandHandler("courses", courses_command))
        app.add_handler(CommandHandler("prices", prices_command))
        app.add_handler(CommandHandler("teachers", teachers_command))
        app.add_handler(CommandHandler("reviews", reviews_command))
        app.add_handler(CommandHandler("faq", faq_command))
        app.add_handler(CommandHandler("contact", contact_command))

        if Config.ENABLE_BOOKING:
            app.add_handler(CommandHandler("book", book_command))

        # Register callback query handler (for inline buttons)
        app.add_handler(CallbackQueryHandler(button_callback))

        # Register message handler for booking flow and AI chat
        async def message_router(update: Update, context) -> None:
            """Route messages to appropriate handler based on state."""
            state = ConversationManager.get_state(context)

            # Check if in booking flow
            if ConversationManager.is_in_booking_flow(context):
                await handle_booking_input(update, context)
            elif Config.ENABLE_AI_CHAT:
                # Regular AI conversation
                await handle_message(update, context)
            else:
                # AI chat disabled
                await update.message.reply_text(
                    "Используйте команды меню для навигации. /help для списка команд."
                )

        app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
                message_router
            )
        )

        logger.info("All handlers registered successfully")

        # Log knowledge base status
        kb_files = ["company", "courses", "teachers", "testimonials", "pricing", "faq", "policies"]
        loaded_files = []
        for kb_file in kb_files:
            if Config.get_knowledge_file(f"{kb_file}.txt"):
                loaded_files.append(kb_file)

        logger.info(f"Knowledge base loaded: {len(loaded_files)}/{len(kb_files)} files")
        if loaded_files:
            logger.info(f"Loaded: {', '.join(loaded_files)}")

        # Start the bot
        logger.info("Starting bot polling...")
        app.run_polling(drop_pending_updates=True)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your environment variables in .env file")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
