"""
Input validation utilities for SpeakFlow English bot.

Provides validation functions for email, phone, name, and other user inputs.
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message). Error message is empty if valid.
    """
    email = email.strip()

    if not email:
        return False, "Email не может быть пустым"

    if len(email) > 254:
        return False, "Email слишком длинный"

    # Basic email regex pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(pattern, email):
        return False, "Некорректный формат email. Пример: example@mail.com"

    return True, ""


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number (Russian or international format).

    Args:
        phone: Phone number to validate

    Returns:
        Tuple of (is_valid, error_message). Error message is empty if valid.
    """
    phone = phone.strip()

    if not phone:
        return True, ""  # Phone is optional

    # Remove common separators
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)

    # Check for valid characters (digits and +)
    if not re.match(r"^\+?[\d]+$", cleaned):
        return False, "Телефон может содержать только цифры, +, -, ( )"

    # Check length (reasonable range for phone numbers)
    if len(cleaned) < 10:
        return False, "Телефон слишком короткий (минимум 10 цифр)"

    if len(cleaned) > 15:
        return False, "Телефон слишком длинный (максимум 15 цифр)"

    # Validate Russian phone format if it starts with +7 or 8
    if cleaned.startswith("+7") or cleaned.startswith("8"):
        if len(cleaned) < 11:
            return (
                False,
                "Неверный формат российского номера. Пример: +7 900 123 45 67",
            )

    return True, ""


def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate user name.

    Args:
        name: Name to validate

    Returns:
        Tuple of (is_valid, error_message). Error message is empty if valid.
    """
    name = name.strip()

    if not name:
        return False, "Имя не может быть пустым"

    if len(name) < 2:
        return False, "Имя слишком короткое (минимум 2 символа)"

    if len(name) > 100:
        return False, "Имя слишком длинное (максимум 100 символов)"

    # Allow letters (including Cyrillic), spaces, hyphens
    if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", name):
        return (
            False,
            "Имя может содержать только буквы, пробелы и дефисы",
        )

    return True, ""


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input to prevent injection attacks.

    Args:
        text: User input text
        max_length: Maximum allowed length

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove control characters except newlines and tabs
    sanitized = "".join(char for char in text if ord(char) >= 32 or char in "\n\t")

    # Trim to max length
    sanitized = sanitized[:max_length]

    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    return sanitized


def validate_text_length(
    text: str, min_length: int = 1, max_length: int = 1000
) -> Tuple[bool, str]:
    """
    Validate text length.

    Args:
        text: Text to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length

    Returns:
        Tuple of (is_valid, error_message). Error message is empty if valid.
    """
    text = text.strip()

    if len(text) < min_length:
        return False, f"Текст слишком короткий (минимум {min_length} символов)"

    if len(text) > max_length:
        return False, f"Текст слишком длинный (максимум {max_length} символов)"

    return True, ""
