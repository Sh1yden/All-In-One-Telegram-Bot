from aiogram.types import Message, CallbackQuery, User
from aiogram import Router
from fluentogram import TranslatorRunner

from src.filters import WeatherCallback

from src.services.WeatherService import WeatherService

from src.keyboards import get_btns_weather, get_btns_weather_now, get_btns_start
from src.core.Logging import get_logger


router = Router()
_lg = get_logger()

_lg.debug("CALLBACK MODULE LOADED - ROUTER CREATED.")


@router.callback_query(WeatherCallback.filter())
async def weather_callback_handler(
    callback: CallbackQuery, callback_data: WeatherCallback, locale: TranslatorRunner
) -> None:
    """Handle weather menu callbacks"""

    _lg.debug(f"CALLBACK HANDLER CALLED!")
    _lg.debug(f"Action: {callback_data.action}")
    _lg.debug(f"User: {callback.from_user.id}")
    _lg.debug(f"Message exists: {callback.message is not None}")
    _lg.debug(f"CALLBACK HANDLER TRIGGERED: {callback_data.action}")

    # Проверяем, что сообщение доступно для редактирования
    if not isinstance(callback.message, Message):
        _lg.warning("Cannot edit inaccessible message.")
        await callback.answer(locale.message_service_error_not_edit())
        return

    message: Message | None = callback.message
    user: User | None = callback.from_user

    try:
        # 📚 Вызов всего меню
        if callback_data.action == "weather_menu":
            await message.edit_text(
                text=locale.message_weather_menu(),
                reply_markup=get_btns_weather(user.id, locale),
            )

        # 🌡 Сейчас
        elif callback_data.action == "weather_now":
            wnm = "FIX USER"
            await message.edit_text(text=wnm, reply_markup=get_btns_weather_now(locale))

        # 📊 Почасовой
        elif callback_data.action == "weather_hours":
            await message.edit_text(
                text=locale.message_service_in_development(),
                reply_markup=get_btns_weather_now(locale),
            )

        # 📆 На 5 дней
        elif callback_data.action == "weather_5d":
            await message.edit_text(
                text=locale.message_service_in_development(),
                reply_markup=get_btns_weather_now(locale),
            )

        # 🌅 Утро / 🌇 Вечер
        elif callback_data.action == "weather_day_night":
            await message.edit_text(
                text=locale.message_service_in_development(),
                reply_markup=get_btns_weather_now(locale),
            )

        # 🌦 Осадки
        elif callback_data.action == "weather_rain":
            await message.edit_text(
                text=locale.message_service_in_development(),
                reply_markup=get_btns_weather_now(locale),
            )

        # 🧭 Ветер/давление
        elif callback_data.action == "weather_wind_pressure":
            await message.edit_text(
                text=locale.message_service_in_development(),
                reply_markup=get_btns_weather_now(locale),
            )

        # ⚙️ Настроить
        elif callback_data.action == "weather_settings":
            await message.edit_text(
                text=locale.message_service_in_development(),
                reply_markup=get_btns_weather_now(locale),
            )

        # 🔔 Подписка
        elif callback_data.action == "weather_subscription":
            await message.edit_text(
                text=locale.message_service_in_development(),
                reply_markup=get_btns_weather_now(locale),
            )

        # 📍 Локация
        elif callback_data.action == "weather_location":
            location_display = "FIX USER"
            await message.answer(text=location_display)

        # 🔙 Назад
        elif callback_data.action == "weather_get_back":
            full_name_user = user.full_name
            main_menu_text = (
                f"{locale.message_start_hello()}"
                f"{full_name_user or 'Пользователь'}"
                f"{locale.message_start_main_menu()}"
            )

            await message.edit_text(
                text=main_menu_text,
                reply_markup=get_btns_start(locale),
            )

        # Ответ что callback обработан
        await callback.answer()

    except Exception as e:
        _lg.error(f"Error in callback handler: {e}")
        await callback.answer(locale.message_service_error_not_edit(), show_alert=True)
