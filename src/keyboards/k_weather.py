from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.callbacks.WeatherCallback import WeatherCallback
from src.config.TextMessages import get_message


def get_inl_btns_weather() -> InlineKeyboardMarkup:
    """Кнопки снизу сообщения после команды /weather."""

    builder = InlineKeyboardBuilder()

    # 🌡 Сейчас     📊 Почасовой
    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][0],
            callback_data=WeatherCallback(action="weather_now").pack(),
        ),
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][1],
            callback_data=WeatherCallback(action="weather_hours").pack(),
        ),
    )

    # 🌅 Утро / 🌇 Вечер
    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][3],
            callback_data=WeatherCallback(action="weather_day_night").pack(),
        ),
    )

    # 📆 На 5 дней
    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][2],
            callback_data=WeatherCallback(action="weather_5d").pack(),
        ),
    )

    # 🌦 Осадки     🧭 Ветер/давление
    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][4],
            callback_data=WeatherCallback(action="weather_rain").pack(),
        ),
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][5],
            callback_data=WeatherCallback(action="weather_wind_pressure").pack(),
        ),
    )

    # 📍 Локация:
    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][8]
            + "Ваш город",  # ! заглушка
            callback_data=WeatherCallback(action="weather_location").pack(),
        ),
    )

    # ⚙️ Настроить  🔔 Подписка
    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][6],
            callback_data=WeatherCallback(action="weather_settings").pack(),
        ),
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][7],
            callback_data=WeatherCallback(action="weather_subscription").pack(),
        ),
    )

    # 🔙 Назад
    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["weather_m"]["buttons"][9],
            callback_data=WeatherCallback(action="weather_get_back").pack(),
        ),
    )

    return builder.as_markup(resize_keyboard=True)
