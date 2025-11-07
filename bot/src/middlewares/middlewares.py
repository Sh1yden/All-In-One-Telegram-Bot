"""Bot middlewares"""

from typing import Any, Awaitable, Callable, Dict

from fluentogram import TranslatorHub
from aiogram import BaseMiddleware
from aiogram.types import Update
from cachetools import TTLCache

# from src.models.user import UserSchema

caches = {"default": TTLCache(maxsize=10_000, ttl=0.1)}


class TranslateMiddleware(BaseMiddleware):  # pylint: disable=too-few-public-methods
    """
    Fluentogram translation middleware
    """

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        language = data["user"].language_code if "user" in data else "ru"

        hub: TranslatorHub = data.get("t_hub")

        data["locale"] = hub.get_translator_by_locale(language)

        return await handler(event, data)
