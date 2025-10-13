from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.callbacks.WeatherCallback import WeatherCallback
from src.config.TextMessages import get_message


def get_inl_btns_weather_now() -> InlineKeyboardMarkup:
    """Кнопки снизу сообщения после команды /weatherNow."""

    builder = InlineKeyboardBuilder()

    # 🔙 Назад
    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][9],
            callback_data=WeatherCallback(action="weather_menu").pack(),
        ),
    )

    return builder.as_markup(resize_keyboard=True)
