from aiogram.types import Message, CallbackQuery, InaccessibleMessage, User
from aiogram.filters import Command
from aiogram import Router

from src.callbacks.WeatherCallback import WeatherCallback  # CALLBACK

from src.services.UserDataService import user_data_service
from src.services.WeatherService import WeatherService  # API # TODO

# from src.services.GeocodingOMAPI import GeocodingOMAPI  # API


from src.keyboards.k_weather import get_inl_btns_weather  # BTN
from src.keyboards.k_weather_now import get_inl_btns_weather_now  # BTN
from src.keyboards.k_start import get_inl_btns_start  # BTN
from src.keyboards.k_device import get_inl_btns_device  # BTN
from src.core.Logging import get_logger
from src.config.TextMessages import get_message


router = Router()
_lg = get_logger()


# обработка нажатия кнопки Погода
@router.callback_query(WeatherCallback.filter())
async def weather_callback_handler(
    callback: CallbackQuery, callback_data: WeatherCallback
):

    # load_msg = WeatherService.get_loading_message()
    # _lg.debug(f"load_message {load_msg}")

    # Проверяем, что сообщение доступно для редактирования
    if isinstance(callback.message, InaccessibleMessage):
        _lg.warning("Cannot edit inaccessible message.")
        await callback.answer("Сообщение нельзя изменить.")
        return

    message: Message | None = callback.message
    user: User | None = callback.from_user

    # 📚 Вызов всего меню
    if callback_data.action == "weather_menu":

        await message.edit_text(
            text=get_message("RU_LN")["weather_m"]["message"],
            reply_markup=get_inl_btns_weather(user.id),
        )

    # 🌡 Сейчас
    if callback_data.action == "weather_now":

        # Проверить наличие локации в файле
        if not user_data_service.user_has_location(user.id):
            await message.answer(
                get_message("RU_LN")["location_m"]["message_loc_not_post"]
            )
            return

        all_w_info = WeatherService().get_weather_now(user.id)
        _lg.debug(f"ALL INFO weather now serv - {all_w_info}")

        await message.edit_text(
            text=str(all_w_info), reply_markup=get_inl_btns_weather_now()
        )

    # 📊 Почасовой
    if callback_data.action == "weather_hours":
        await message.edit_text(
            text=get_message("RU_LN")["service_m"]["message_in_development"],
            reply_markup=get_inl_btns_weather_now(),
        )
        await WeatherService.get_weather_hours()

    # 📆 На 5 дней
    if callback_data.action == "weather_5d":
        await message.edit_text(
            text=get_message("RU_LN")["service_m"]["message_in_development"],
            reply_markup=get_inl_btns_weather_now(),
        )
        await WeatherService.get_weather_5d()

    # 🌅 Утро / 🌇 Вечер
    if callback_data.action == "weather_day_night":
        await message.edit_text(
            text=get_message("RU_LN")["service_m"]["message_in_development"],
            reply_markup=get_inl_btns_weather_now(),
        )
        await WeatherService.get_weather_day_night()

    # 🌦 Осадки
    if callback_data.action == "weather_rain":
        await message.edit_text(
            text=get_message("RU_LN")["service_m"]["message_in_development"],
            reply_markup=get_inl_btns_weather_now(),
        )
        await WeatherService.get_weather_rain()

    # 🧭 Ветер/давление
    if callback_data.action == "weather_wind_pressure":
        await message.edit_text(
            text=get_message("RU_LN")["service_m"]["message_in_development"],
            reply_markup=get_inl_btns_weather_now(),
        )
        await WeatherService.get_weather_wind_pressure()

    # ⚙️ Настроить
    if callback_data.action == "weather_settings":
        await message.edit_text(
            text=get_message("RU_LN")["service_m"]["message_in_development"],
            reply_markup=get_inl_btns_weather_now(),
        )

    # Функции на потом
    # 🔔 Подписка
    if callback_data.action == "weather_subscription":
        await message.edit_text(
            text=get_message("RU_LN")["service_m"]["message_in_development"],
            reply_markup=get_inl_btns_weather_now(),
        )

    # 📍 Локация:
    if callback_data.action == "weather_location":

        # TODO сделать так чтобы не писало новое сообщение а изменялось меню на это
        # TODO сделать чтобы после взаимодействия с меню локации оно заменялось обратно на погодное

        if not user_data_service.user_has_location(user.id):
            # Переброс на выбор платформы для правильного определения местоположения
            await message.answer(
                text=get_message("RU_LN")["device_m"]["message"],
                reply_markup=get_inl_btns_device(),
            )
        else:
            # Показать сохраненную локацию
            location_display = user_data_service.format_user_location(user.id)
            # TODO добавить изменение локации и её сброс
            await message.answer(
                text=location_display,
            )

    # 🔙 Назад
    if callback_data.action == "weather_get_back":

        full_name_user = callback.from_user.full_name

        main_menu_text = f"""{get_message("RU_LN")["start_m"]["message_hello"]}<b>{full_name_user or "Пользователь"}</b>{get_message("RU_LN")["start_m"]["message_main_menu"]}"""
        _lg.debug(f"{main_menu_text}")

        await message.edit_text(
            text=main_menu_text,
            reply_markup=get_inl_btns_start(),
        )


# обработка команды /weatherMenu
@router.message(Command("weatherMenu"))
async def command_weather_handler(message: Message):

    user: User | None = message.from_user

    await message.answer(
        text=get_message("RU_LN")["weather_m"]["message"],
        reply_markup=get_inl_btns_weather(user.id),
    )
