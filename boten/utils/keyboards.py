"""
Inline keyboard builders for SpeakFlow English bot.

Provides reusable keyboard layouts for navigation and user interaction.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Create main menu inline keyboard.

    Returns:
        InlineKeyboardMarkup with main menu buttons
    """
    keyboard = [
        [
            InlineKeyboardButton("📚 Курсы", callback_data="menu_courses"),
            InlineKeyboardButton("💰 Цены", callback_data="menu_prices"),
            InlineKeyboardButton("👨‍🏫 Преподаватели", callback_data="menu_teachers"),
        ],
        [
            InlineKeyboardButton("📅 Расписание", callback_data="menu_schedule"),
            InlineKeyboardButton("⭐ Отзывы", callback_data="menu_reviews"),
            InlineKeyboardButton("❓ FAQ", callback_data="menu_faq"),
        ],
        [
            InlineKeyboardButton("📝 Записаться", callback_data="menu_book"),
            InlineKeyboardButton("📞 Контакты", callback_data="menu_contact"),
            InlineKeyboardButton("💬 Чат с AI", callback_data="menu_chat"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_courses_keyboard() -> InlineKeyboardMarkup:
    """
    Create courses selection keyboard.

    Returns:
        InlineKeyboardMarkup with course categories
    """
    keyboard = [
        [InlineKeyboardButton("📘 Общий английский", callback_data="courses_general")],
        [
            InlineKeyboardButton(
                "🗣️ Speaking Booster", callback_data="course_speaking"
            ),
            InlineKeyboardButton(
                "💼 Business English", callback_data="course_business"
            ),
        ],
        [
            InlineKeyboardButton("🎯 IELTS/TOEFL", callback_data="course_exam"),
            InlineKeyboardButton("💻 IT English", callback_data="course_it"),
        ],
        [
            InlineKeyboardButton("✈️ Для переезда", callback_data="course_relocation")
        ],
        [InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_general_english_keyboard() -> InlineKeyboardMarkup:
    """
    Create general English levels keyboard.

    Returns:
        InlineKeyboardMarkup with English levels
    """
    keyboard = [
        [InlineKeyboardButton("📗 Beginner (A1-A2)", callback_data="course_a1a2")],
        [InlineKeyboardButton("📙 Intermediate (B1-B2)", callback_data="course_b1b2")],
        [InlineKeyboardButton("📕 Advanced (C1)", callback_data="course_c1")],
        [InlineKeyboardButton("⬅️ Назад к курсам", callback_data="menu_courses")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_faq_categories_keyboard() -> InlineKeyboardMarkup:
    """
    Create FAQ categories keyboard.

    Returns:
        InlineKeyboardMarkup with FAQ categories
    """
    keyboard = [
        [
            InlineKeyboardButton("📖 О курсах", callback_data="faq_courses"),
            InlineKeyboardButton("💳 Оплата", callback_data="faq_payment"),
        ],
        [
            InlineKeyboardButton("📅 Расписание", callback_data="faq_schedule"),
            InlineKeyboardButton("👥 Группы", callback_data="faq_groups"),
        ],
        [
            InlineKeyboardButton("🎓 Сертификаты", callback_data="faq_certificates"),
            InlineKeyboardButton("💻 Техподдержка", callback_data="faq_support"),
        ],
        [InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_booking_time_keyboard() -> InlineKeyboardMarkup:
    """
    Create time slot selection keyboard for booking.

    Returns:
        InlineKeyboardMarkup with time slot options
    """
    keyboard = [
        [InlineKeyboardButton("🌅 Утро (08:00-09:00)", callback_data="time_morning")],
        [InlineKeyboardButton("☀️ День (13:00-14:00)", callback_data="time_afternoon")],
        [
            InlineKeyboardButton("🌙 Вечер (19:00-20:00)", callback_data="time_evening")
        ],
        [
            InlineKeyboardButton(
                "🌃 Поздний вечер (20:30-21:30)", callback_data="time_late"
            )
        ],
        [InlineKeyboardButton("❌ Отменить", callback_data="booking_cancel")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_booking_courses_keyboard() -> InlineKeyboardMarkup:
    """
    Create course selection keyboard for booking.

    Returns:
        InlineKeyboardMarkup with available courses
    """
    keyboard = [
        [InlineKeyboardButton("General English A1-A2", callback_data="book_a1a2")],
        [InlineKeyboardButton("General English B1-B2", callback_data="book_b1b2")],
        [InlineKeyboardButton("Speaking Booster", callback_data="book_speaking")],
        [InlineKeyboardButton("Business English", callback_data="book_business")],
        [InlineKeyboardButton("IELTS/TOEFL Preparation", callback_data="book_exam")],
        [InlineKeyboardButton("IT English", callback_data="book_it")],
        [InlineKeyboardButton("English for Relocation", callback_data="book_relocation")],
        [InlineKeyboardButton("❌ Отменить", callback_data="booking_cancel")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Create simple 'back to menu' keyboard.

    Returns:
        InlineKeyboardMarkup with back button
    """
    keyboard = [[InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")]]
    return InlineKeyboardMarkup(keyboard)


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Create cancel button keyboard.

    Returns:
        InlineKeyboardMarkup with cancel button
    """
    keyboard = [[InlineKeyboardButton("❌ Отменить", callback_data="booking_cancel")]]
    return InlineKeyboardMarkup(keyboard)


def get_confirm_keyboard(action: str = "confirm") -> InlineKeyboardMarkup:
    """
    Create confirmation keyboard with yes/no options.

    Args:
        action: Action prefix for callback data

    Returns:
        InlineKeyboardMarkup with confirm/cancel buttons
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Подтвердить", callback_data=f"{action}_yes"),
            InlineKeyboardButton("❌ Отменить", callback_data=f"{action}_no"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
