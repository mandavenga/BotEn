"""
AI Service wrapper for OpenRouter API integration.

Provides retry logic, caching, error handling, and context-aware prompts.
"""

import time
from typing import List, Dict, Optional
from openai import OpenAI

from config import Config
from utils.logger import setup_logger, log_error, log_ai_response

logger = setup_logger("ai_service")


class AIService:
    """Wrapper for OpenRouter API with enhanced features."""

    def __init__(self):
        """Initialize AI service with OpenRouter client."""
        self.client = OpenAI(
            base_url=Config.OPENROUTER_BASE_URL,
            api_key=Config.OPENROUTER_API_KEY,
        )
        self._cache: Dict[str, tuple[str, float]] = {}  # Simple in-memory cache

    def get_response(
        self,
        messages: List[Dict[str, str]],
        user_id: int,
        context: str = "general",
        use_cache: bool = True,
    ) -> str:
        """
        Get AI response with retry logic and caching.

        Args:
            messages: List of message dicts with 'role' and 'content'
            user_id: Telegram user ID for logging
            context: Context type (general, booking, faq)
            use_cache: Whether to use caching for this request

        Returns:
            AI response text
        """
        start_time = time.time()

        # Create cache key from last user message
        cache_key = None
        if use_cache and messages:
            last_message = next(
                (m["content"] for m in reversed(messages) if m["role"] == "user"), None
            )
            if last_message:
                cache_key = f"{context}:{last_message[:100]}"
                cached = self._get_cached_response(cache_key)
                if cached:
                    logger.info(f"Cache hit for user {user_id}")
                    return cached

        # Build system prompt based on context
        system_prompt = self._build_system_prompt(context)

        # Prepare messages for API
        api_messages = [{"role": "system", "content": system_prompt}] + messages

        # Try with retries
        for attempt in range(Config.AI_RETRY_ATTEMPTS):
            try:
                response = self.client.chat.completions.create(
                    model=Config.OPENROUTER_MODEL,
                    messages=api_messages,
                    max_tokens=Config.AI_MAX_TOKENS,
                    temperature=Config.AI_TEMPERATURE,
                    extra_headers={
                        "X-Title": Config.BOT_NAME,
                    },
                )

                response_text = (
                    response.choices[0].message.content
                    or "Извините, не смог сформировать ответ."
                )

                # Cache the response
                if cache_key:
                    self._cache_response(cache_key, response_text)

                # Log success
                elapsed = time.time() - start_time
                log_ai_response(logger, user_id, elapsed, success=True)

                return response_text

            except Exception as e:
                logger.warning(
                    f"AI request attempt {attempt + 1}/{Config.AI_RETRY_ATTEMPTS} failed: {e}"
                )

                if attempt == Config.AI_RETRY_ATTEMPTS - 1:
                    # Last attempt failed
                    log_error(logger, e, "AI service")
                    elapsed = time.time() - start_time
                    log_ai_response(logger, user_id, elapsed, success=False)
                    return self._get_fallback_response()

                # Wait before retry (exponential backoff)
                time.sleep(2**attempt)

        return self._get_fallback_response()

    def _build_system_prompt(self, context: str) -> str:
        """
        Build context-specific system prompt.

        Args:
            context: Context type (general, booking, faq)

        Returns:
            System prompt text
        """
        # Load knowledge base files
        knowledge_base = self._load_knowledge_base()

        base_prompt = (
            "Ты полезный AI-помощник онлайн-школы английского языка SpeakFlow English. "
            "Отвечай на вопросы ТОЛЬКО на основе предоставленной базы знаний. "
            "Если ответа нет в базе знаний, вежливо скажи, что у тебя нет этой информации, "
            "и предложи клиенту связаться с поддержкой напрямую.\n"
            "Отвечай на том же языке, на котором пишет пользователь.\n"
            "Будь дружелюбным, профессиональным и полезным.\n\n"
        )

        # Context-specific instructions
        if context == "booking":
            base_prompt += (
                "Ты помогаешь пользователю записаться на пробное занятие. "
                "Будь внимательным и помогай на каждом шаге процесса бронирования.\n\n"
            )
        elif context == "faq":
            base_prompt += (
                "Отвечай на частые вопросы клиентов, используя информацию из раздела FAQ.\n\n"
            )

        base_prompt += "=== БАЗА ЗНАНИЙ ===\n" f"{knowledge_base}\n" "=== КОНЕЦ БАЗЫ ЗНАНИЙ ==="

        return base_prompt

    def _load_knowledge_base(self) -> str:
        """
        Load all knowledge base files.

        Returns:
            Combined knowledge base text
        """
        knowledge_files = [
            "company.txt",
            "courses.txt",
            "teachers.txt",
            "testimonials.txt",
            "pricing.txt",
            "faq.txt",
            "policies.txt",
        ]

        knowledge_parts = []

        for filename in knowledge_files:
            path = Config.get_knowledge_file(filename)
            if path:
                try:
                    content = path.read_text(encoding="utf-8").strip()
                    if content:
                        knowledge_parts.append(content)
                except Exception as e:
                    logger.warning(f"Failed to load {filename}: {e}")

        # Fallback to old knowledge_base.txt if new files don't exist
        if not knowledge_parts:
            old_kb_path = Config.BASE_DIR / "knowledge_base.txt"
            if old_kb_path.exists():
                try:
                    content = old_kb_path.read_text(encoding="utf-8").strip()
                    knowledge_parts.append(content)
                except Exception as e:
                    logger.warning(f"Failed to load knowledge_base.txt: {e}")

        if not knowledge_parts:
            return "База знаний не загружена."

        return "\n\n".join(knowledge_parts)

    def _get_cached_response(self, cache_key: str) -> Optional[str]:
        """
        Get cached response if not expired.

        Args:
            cache_key: Cache key

        Returns:
            Cached response or None if not found/expired
        """
        if cache_key in self._cache:
            response, timestamp = self._cache[cache_key]
            if time.time() - timestamp < Config.AI_CACHE_TTL:
                return response
            else:
                # Remove expired cache entry
                del self._cache[cache_key]

        return None

    def _cache_response(self, cache_key: str, response: str) -> None:
        """
        Cache a response.

        Args:
            cache_key: Cache key
            response: Response to cache
        """
        self._cache[cache_key] = (response, time.time())

        # Simple cache size management - keep last 100 entries
        if len(self._cache) > 100:
            # Remove oldest entries
            sorted_keys = sorted(self._cache.items(), key=lambda x: x[1][1])
            for key, _ in sorted_keys[:20]:  # Remove 20 oldest
                del self._cache[key]

    def _get_fallback_response(self) -> str:
        """
        Get fallback response when AI is unavailable.

        Returns:
            Fallback message
        """
        return (
            "😔 Извините, AI-помощник временно недоступен. "
            "Пожалуйста, попробуйте через несколько минут или свяжитесь с нашей поддержкой:\n\n"
            "📧 support@speakflow-english.com\n"
            "📱 +7 495 123 45 67\n\n"
            "Мы работаем Пн-Пт с 10:00 до 19:00 МСК."
        )

    def clear_cache(self) -> None:
        """Clear the response cache."""
        self._cache.clear()
        logger.info("AI response cache cleared")
