from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.callbacks.WeatherCallback import WeatherCallback


def get_inl_btns_weather() -> InlineKeyboardMarkup:
    """Кнопки снизу сообщения после команды /weather."""

    builder = InlineKeyboardBuilder()

    # добавить еще кнопок для других функций
    builder.row(
        InlineKeyboardButton(
            text="Локация",
            callback_data=WeatherCallback(action="weather_get_location").pack(),
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=WeatherCallback(action="weather_get_back").pack(),
        ),
    )

    return builder.as_markup()
