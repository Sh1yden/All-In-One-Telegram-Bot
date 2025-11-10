from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from src.filters import WeatherCallback


def get_btns_weather_now(locale: TranslatorRunner) -> InlineKeyboardMarkup:
    """Кнопки снизу сообщения после команды /weatherNow."""

    builder = InlineKeyboardBuilder()

    # 🔙 Назад
    builder.row(
        InlineKeyboardButton(
            text=locale.button_weather_now_back(),
            callback_data=WeatherCallback(action="weather_menu").pack(),
        ),
    )

    return builder.as_markup(resize_keyboard=True)
