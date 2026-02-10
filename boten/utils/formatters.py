"""
Message formatting utilities for SpeakFlow English bot.

Provides consistent message formatting across all bot responses.
"""

from typing import Dict, List, Optional


def format_welcome_message() -> str:
    """
    Format welcome message for /start command.

    Returns:
        Formatted welcome message
    """
    return (
        "👋 Добро пожаловать в SpeakFlow English!\n\n"
        "Я AI-помощник онлайн-школы английского языка. "
        "Помогу вам узнать о наших курсах, преподавателях, ценах "
        "и записаться на пробное занятие.\n\n"
        "Выберите интересующий раздел в меню ниже или задайте вопрос в чате 👇"
    )


def format_help_message() -> str:
    """
    Format help message with all available commands.

    Returns:
        Formatted help message
    """
    commands = [
        ("/start", "Начать работу с ботом"),
        ("/help", "Показать список всех команд"),
        ("/menu", "Открыть главное меню"),
        ("/courses", "Каталог курсов"),
        ("/prices", "Цены и акции"),
        ("/teachers", "Наши преподаватели"),
        ("/faq", "Часто задаваемые вопросы"),
        ("/book", "Записаться на пробное занятие"),
        ("/reviews", "Отзывы студентов"),
        ("/contact", "Контактная информация"),
        ("/reset", "Очистить историю разговора"),
    ]

    message = "📋 <b>Доступные команды:</b>\n\n"
    for cmd, description in commands:
        message += f"{cmd} - {description}\n"

    message += "\n💬 Вы также можете задать любой вопрос в чате!"

    return message


def format_course_info(course_data: str) -> str:
    """
    Format course information message.

    Args:
        course_data: Raw course data from knowledge base

    Returns:
        Formatted course info
    """
    # Simple formatting for now - can be enhanced later
    return f"📚 <b>Информация о курсе</b>\n\n{course_data}"


def format_teacher_bio(teacher_data: str) -> str:
    """
    Format teacher biography.

    Args:
        teacher_data: Raw teacher data from knowledge base

    Returns:
        Formatted teacher bio
    """
    return f"👨‍🏫 <b>Наши преподаватели</b>\n\n{teacher_data}"


def format_price_table(price_data: str) -> str:
    """
    Format pricing information.

    Args:
        price_data: Raw price data from knowledge base

    Returns:
        Formatted price table
    """
    return f"💰 <b>Цены и тарифы</b>\n\n{price_data}"


def format_testimonial(testimonial_data: str) -> str:
    """
    Format student testimonial.

    Args:
        testimonial_data: Raw testimonial data from knowledge base

    Returns:
        Formatted testimonial
    """
    return f"⭐ <b>Отзывы студентов</b>\n\n{testimonial_data}"


def format_contact_info() -> str:
    """
    Format contact information message.

    Returns:
        Formatted contact info
    """
    return (
        "📞 <b>Контактная информация</b>\n\n"
        "🌐 Сайт: https://speakflow-english.com\n"
        "📧 Email: support@speakflow-english.com\n"
        "📱 Телефон: +7 495 123 45 67\n\n"
        "⏰ <b>Часы работы поддержки:</b>\n"
        "Понедельник – Пятница: 10:00 – 19:00 МСК\n\n"
        "💬 Telegram-бот работает 24/7"
    )


def format_booking_confirmation(
    name: str, course: str, time: str, email: str, phone: Optional[str] = None
) -> str:
    """
    Format booking confirmation message.

    Args:
        name: Student name
        course: Selected course
        time: Selected time slot
        email: Student email
        phone: Student phone (optional)

    Returns:
        Formatted confirmation message
    """
    message = (
        "✅ <b>Запись на пробное занятие подтверждена!</b>\n\n"
        f"👤 Имя: {name}\n"
        f"📚 Курс: {course}\n"
        f"⏰ Время: {time}\n"
        f"📧 Email: {email}\n"
    )

    if phone:
        message += f"📱 Телефон: {phone}\n"

    message += (
        "\n📩 На ваш email отправлено письмо с подтверждением и ссылкой на Zoom.\n\n"
        "До встречи на занятии! 🎉"
    )

    return message


def format_error_message(error_type: str = "general") -> str:
    """
    Format user-friendly error message.

    Args:
        error_type: Type of error (general, api, timeout, validation)

    Returns:
        Formatted error message
    """
    messages = {
        "general": "😔 Произошла ошибка. Пожалуйста, попробуйте позже или обратитесь в поддержку.",
        "api": "🤖 AI-помощник временно недоступен. Попробуйте через несколько минут.",
        "timeout": "⏱️ Превышено время ожидания. Пожалуйста, попробуйте снова.",
        "validation": "⚠️ Проверьте правильность введённых данных.",
    }

    return messages.get(error_type, messages["general"])


def format_faq_category(category: str, questions: List[str]) -> str:
    """
    Format FAQ category with questions.

    Args:
        category: Category name
        questions: List of questions in the category

    Returns:
        Formatted FAQ section
    """
    message = f"❓ <b>{category}</b>\n\n"

    for i, question in enumerate(questions, 1):
        message += f"{i}. {question}\n"

    return message


def split_long_message(text: str, max_length: int = 4096) -> List[str]:
    """
    Split long message into multiple parts respecting Telegram's limit.

    Args:
        text: Message text to split
        max_length: Maximum length per message (default: Telegram's 4096)

    Returns:
        List of message parts
    """
    if len(text) <= max_length:
        return [text]

    parts = []
    current_part = ""

    # Split by paragraphs first
    paragraphs = text.split("\n\n")

    for paragraph in paragraphs:
        if len(current_part) + len(paragraph) + 2 <= max_length:
            current_part += paragraph + "\n\n"
        else:
            if current_part:
                parts.append(current_part.strip())
            current_part = paragraph + "\n\n"

    if current_part:
        parts.append(current_part.strip())

    return parts


def format_schedule_info() -> str:
    """
    Format schedule information message.

    Returns:
        Formatted schedule info
    """
    return (
        "📅 <b>Расписание занятий</b>\n\n"
        "<b>Групповые занятия:</b>\n"
        "🌅 Утро: 08:00 – 09:00 МСК\n"
        "☀️ День: 13:00 – 14:00 МСК\n"
        "🌙 Вечер: 19:00 – 20:00 МСК\n"
        "🌃 Поздний вечер: 20:30 – 21:30 МСК\n\n"
        "<b>Speaking Clubs:</b>\n"
        "Суббота: 11:00 и 18:00 МСК\n\n"
        "📍 Все занятия проходят в Zoom\n"
        "⏰ Расписание подбирается с учётом вашего часового пояса"
    )
