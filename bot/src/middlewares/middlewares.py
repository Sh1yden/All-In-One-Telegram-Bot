"""Bot middlewares"""

from typing import Any, Awaitable, Callable, Dict

from fluentogram import TranslatorHub
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Update, Message, CallbackQuery
from cachetools import TTLCache

from src.core import get_logger


caches = {"default": TTLCache(maxsize=10_000, ttl=0.1)}
_lg = get_logger()


class TranslateMiddleware(BaseMiddleware):
    """Fluentogram translation middleware"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        _lg.debug(f"Middleware called for event type: {type(event).__name__}")

        # Проверяем что внутри Update
        if isinstance(event, Update):
            _lg.debug(f"Update ID: {event.update_id}")
            _lg.debug(f"Has message: {event.message is not None}")
            _lg.debug(f"Has callback_query: {event.callback_query is not None}")

            if event.callback_query:
                _lg.debug(f"Callback data: {event.callback_query.data}")

        user: User | None = data.get("event_from_user")

        if user:
            language = user.language_code or "ru"
            _lg.debug(f"User {user.id} language: {language}")
        else:
            language = "ru"
            _lg.warning("No user found in event")

        hub: TranslatorHub | None = data.get("t_hub")

        if not hub or hub is None:
            _lg.error("TranslatorHub not found in data")
            raise RuntimeError("TranslatorHub not found in data")

        data["locale"] = hub.get_translator_by_locale(language)
        _lg.debug(f"Locale set: {type(data['locale'])}")

        result = await handler(event, data)
        _lg.debug(f"Handler completed for {type(event).__name__}")

        return result
