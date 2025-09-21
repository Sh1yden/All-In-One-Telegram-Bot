from aiogram.types import Message, CallbackQuery, InaccessibleMessage
from aiogram.filters import Command
from aiogram import Router

from src.callbacks.WeatherCallback import WeatherCallback  # CALLBACK

from src.services.WeatherService import WeatherService  # API # TODO

from src.keyboards.k_weather import get_inl_btns_weather  # BTN # TODO
from src.keyboards.k_start import get_inl_btns_start  # BTN # TODO
from src.core.Logging import get_logger
from src.config.TextMessages import get_message


router = Router()
_lg = get_logger()


# обработка нажатия кнопки Погода
@router.callback_query(WeatherCallback.filter())
async def weather_callback_handler(
    callback: CallbackQuery, callback_data: WeatherCallback
):

    load_msg = WeatherService.get_loading_message()
    _lg.debug(f"load_message {load_msg}")
    # await callback.answer(load_msg)
    # await callback.message.answer(load_msg)

    # current_weather = await WeatherService.get_current_weather()

    # Проверяем, что сообщение доступно для редактирования
    if isinstance(callback.message, InaccessibleMessage):
        _lg.warning("Cannot edit inaccessible message.")
        await callback.answer("Сообщение нельзя изменить.")
        return

    message: Message | None = callback.message

    # 📚 Вызов всего меню
    if callback_data.action == "weather_menu":

        await message.edit_text(
            text=get_message("RU_LN")["weather_m"]["message"],
            reply_markup=get_inl_btns_weather(),
        )

    # 🌡 Сейчас
    if callback_data.action == "weather_now":
        pass

    # 📊 Почасовой
    if callback_data.action == "weather_hours":
        pass

    # 📆 На 5 дней
    if callback_data.action == "weather_5d":
        pass

    # 🌅 Утро / 🌇 Вечер
    if callback_data.action == "weather_day_night":
        pass

    # 🌦 Осадки
    if callback_data.action == "weather_rain":
        pass

    # 🧭 Ветер/давление
    if callback_data.action == "weather_wind_pressure":
        pass

    # ⚙️ Настроить
    if callback_data.action == "weather_settings":
        pass

    # 🔔 Подписка
    if callback_data.action == "weather_subscription":
        pass

    # 📍 Локация:
    if callback_data.action == "weather_location":
        pass

    # 🔙 Назад
    if callback_data.action == "weather_get_back":

        full_name_user = callback.from_user.full_name

        main_menu_text = f"""{get_message("RU_LN")["start_m"]["message1"]}<b>{full_name_user or "Пользователь"}</b>{get_message("RU_LN")["start_m"]["message2"]}"""
        _lg.debug(f"{main_menu_text}")

        await message.edit_text(
            text=main_menu_text,
            reply_markup=get_inl_btns_start(),
        )


# обработка команды /weather_menu
@router.message(Command("weather_menu"))
async def command_weather_handler(message: Message):

    await message.answer(
        text=get_message("RU_LN")["weather_m"]["message"],
        reply_markup=get_inl_btns_weather(),
    )
