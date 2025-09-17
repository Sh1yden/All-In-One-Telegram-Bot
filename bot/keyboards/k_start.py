from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.WeatherCallback import WeatherCallback


def get_inl_btns_start() -> InlineKeyboardMarkup:
    """Кнопки снизу сообщения после команды /start."""

    builder = InlineKeyboardBuilder()

    # добавить еще кнопок для других функций
    builder.row(
        InlineKeyboardButton(
            text="Погода", callback_data=WeatherCallback(action="weather_menu").pack()
        )
    )

    return builder.as_markup()
