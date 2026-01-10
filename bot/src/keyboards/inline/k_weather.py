from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from src.database.repositories import UserRepository

from src.filters import WeatherCallback


async def get_btns_weather(
    user_id: int,
    locale: TranslatorRunner,
    user_repo: UserRepository,
) -> InlineKeyboardMarkup:
    """Кнопки снизу сообщения после команды /weather."""

    builder = InlineKeyboardBuilder()

    # 🌡 Сейчас     📊 Почасовой
    builder.row(
        InlineKeyboardButton(
            text=locale.button_weather_menu_now(),
            callback_data=WeatherCallback(action="weather_now").pack(),
        ),
        InlineKeyboardButton(
            text=locale.button_weather_menu_hours(),
            callback_data=WeatherCallback(action="weather_hours").pack(),
        ),
    )

    # 🌅 Утро / 🌇 Вечер
    builder.row(
        InlineKeyboardButton(
            text=locale.button_weather_menu_day_night(),
            callback_data=WeatherCallback(action="weather_day_night").pack(),
        ),
    )

    # 📆 На 5 дней
    builder.row(
        InlineKeyboardButton(
            text=locale.button_weather_menu_5d(),
            callback_data=WeatherCallback(action="weather_5d").pack(),
        ),
    )

    # 🌦 Осадки     🧭 Ветер/давление
    builder.row(
        InlineKeyboardButton(
            text=locale.button_weather_menu_rain(),
            callback_data=WeatherCallback(action="weather_rain").pack(),
        ),
        InlineKeyboardButton(
            text=locale.button_weather_menu_wind_pressure(),
            callback_data=WeatherCallback(action="weather_wind_pressure").pack(),
        ),
    )

    # 📍 Локация:
    user_data = await user_repo.get_by_id(user_id)
    city = user_data.get("city", "Ваша локация") if user_data else "Ваша локация"
    builder.row(
        InlineKeyboardButton(
            text=locale.button_weather_menu_location() + city,
            callback_data=WeatherCallback(action="weather_location").pack(),
        ),
    )

    # ⚙️ Настроить  🔔 Подписка
    builder.row(
        InlineKeyboardButton(
            text=locale.button_weather_menu_settings(),
            callback_data=WeatherCallback(action="weather_settings").pack(),
        ),
        InlineKeyboardButton(
            text=locale.button_weather_menu_subscription(),
            callback_data=WeatherCallback(action="weather_subscription").pack(),
        ),
    )

    # 🔙 Назад
    builder.row(
        InlineKeyboardButton(
            text=locale.button_weather_menu_back(),
            callback_data=WeatherCallback(action="weather_get_back").pack(),
        ),
    )

    return builder.as_markup(resize_keyboard=True)
