from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.callbacks.WeatherCallback import WeatherCallback
from src.config.TextMessages import get_message


def get_inl_btns_start() -> InlineKeyboardMarkup:
    """Кнопки снизу сообщения после команды /start."""

    builder = InlineKeyboardBuilder()

    # добавить еще кнопок для других функций
    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["start_m"]["buttons"][0],
            callback_data=WeatherCallback(action="weather_menu").pack(),
        )
    )

    return builder.as_markup()
