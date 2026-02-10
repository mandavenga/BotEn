"""
Callback query handler for inline keyboard buttons.

Handles all button presses in inline keyboards.
"""

from telegram import Update
from telegram.ext import ContextTypes

from services.booking_manager import BookingManager
from services.conversation_manager import ConversationManager
from config import Config
from utils.keyboards import (
    get_main_menu_keyboard,
    get_courses_keyboard,
    get_general_english_keyboard,
    get_faq_categories_keyboard,
    get_booking_time_keyboard,
    get_cancel_keyboard,
    get_back_to_menu_keyboard,
)
from utils.logger import setup_logger

logger = setup_logger("handlers.callbacks")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle callback queries from inline keyboard buttons.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    query = update.callback_query
    await query.answer()

    callback_data = query.data
    user_id = update.effective_user.id

    logger.info(f"User {user_id} pressed button: {callback_data}")

    # Main menu navigation
    if callback_data == "back_to_menu":
        keyboard = get_main_menu_keyboard()
        await query.edit_message_text(
            "📋 Главное меню\n\nВыберите интересующий раздел:",
            reply_markup=keyboard
        )

    elif callback_data == "menu_courses":
        keyboard = get_courses_keyboard()
        await query.edit_message_text(
            "📚 Каталог курсов\n\nВыберите категорию:",
            reply_markup=keyboard
        )

    elif callback_data == "menu_prices":
        # Load pricing info
        pricing_path = Config.get_knowledge_file("pricing.txt")
        if pricing_path:
            content = pricing_path.read_text(encoding="utf-8")
            lines = content.split('\n')
            pricing_info = '\n'.join(lines[:80])
        else:
            pricing_info = "Информация о ценах временно недоступна."

        keyboard = get_back_to_menu_keyboard()
        await query.edit_message_text(
            f"💰 <b>Цены и тарифы</b>\n\n{pricing_info}",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback_data == "menu_teachers":
        teachers_path = Config.get_knowledge_file("teachers.txt")
        if teachers_path:
            content = teachers_path.read_text(encoding="utf-8")
            lines = content.split('\n')
            overview = '\n'.join(lines[:100])
        else:
            overview = "Информация о преподавателях временно недоступна."

        keyboard = get_back_to_menu_keyboard()
        await query.edit_message_text(
            f"👨‍🏫 <b>Наши преподаватели</b>\n\n{overview}",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback_data == "menu_schedule":
        from utils.formatters import format_schedule_info
        schedule_text = format_schedule_info()
        keyboard = get_back_to_menu_keyboard()
        await query.edit_message_text(
            schedule_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback_data == "menu_reviews":
        testimonials_path = Config.get_knowledge_file("testimonials.txt")
        if testimonials_path:
            content = testimonials_path.read_text(encoding="utf-8")
            lines = content.split('\n')
            overview = '\n'.join(lines[:120])
        else:
            overview = "Отзывы временно недоступны."

        keyboard = get_back_to_menu_keyboard()
        await query.edit_message_text(
            f"⭐ <b>Отзывы студентов</b>\n\n{overview}",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback_data == "menu_faq":
        keyboard = get_faq_categories_keyboard()
        await query.edit_message_text(
            "❓ <b>Часто задаваемые вопросы</b>\n\nВыберите категорию:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback_data == "menu_contact":
        from utils.formatters import format_contact_info
        contact_text = format_contact_info()
        keyboard = get_back_to_menu_keyboard()
        await query.edit_message_text(
            contact_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback_data == "menu_chat":
        keyboard = get_back_to_menu_keyboard()
        ConversationManager.reset_state(context)
        await query.edit_message_text(
            "💬 <b>Чат с AI-помощником</b>\n\n"
            "Задайте любой вопрос о наших курсах, ценах, преподавателях - "
            "я отвечу на основе базы знаний школы!\n\n"
            "Просто напишите ваш вопрос в чат 👇",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    # Courses navigation
    elif callback_data == "courses_general":
        keyboard = get_general_english_keyboard()
        await query.edit_message_text(
            "📘 <b>Общий английский</b>\n\nВыберите уровень:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback_data.startswith("course_"):
        # Show specific course details
        course_name = callback_data.replace("course_", "")
        keyboard = get_back_to_menu_keyboard()
        await query.edit_message_text(
            f"📚 Информация о курсе '{course_name}'\n\n"
            "Для подробной информации спросите в чате или позвоните нам!",
            reply_markup=keyboard
        )

    # FAQ categories
    elif callback_data.startswith("faq_"):
        category = callback_data.replace("faq_", "")
        keyboard = get_faq_categories_keyboard()
        await query.edit_message_text(
            f"❓ FAQ: {category}\n\n"
            "Задайте конкретный вопрос в чате, и я отвечу!",
            reply_markup=keyboard
        )

    # Booking flow
    elif callback_data == "menu_book":
        BookingManager.start_booking(context)
        from utils.keyboards import get_booking_courses_keyboard
        keyboard = get_booking_courses_keyboard()
        await query.edit_message_text(
            "📝 <b>Запись на пробное занятие</b>\n\n"
            "Шаг 1/5: Выберите курс:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    elif callback_data.startswith("book_"):
        # Course selected for booking
        success = BookingManager.set_course(context, callback_data)
        if success:
            keyboard = get_booking_time_keyboard()
            await query.edit_message_text(
                "✅ Отлично!\n\n"
                "Шаг 2/5: Выберите удобное время:",
                reply_markup=keyboard
            )

    elif callback_data.startswith("time_"):
        # Time selected
        success = BookingManager.set_time(context, callback_data)
        if success:
            await query.edit_message_text(
                "✅ Отлично!\n\n"
                "Шаг 3/5: Введите ваше имя (отправьте сообщением):"
            )

    elif callback_data == "booking_cancel":
        BookingManager.cancel_booking(context)
        keyboard = get_main_menu_keyboard()
        await query.edit_message_text(
            "❌ Бронирование отменено.\n\nВернуться в главное меню:",
            reply_markup=keyboard
        )

    logger.info(f"Callback {callback_data} processed for user {user_id}")
