from aiogram.types import Message, CallbackQuery, InaccessibleMessage, User
from aiogram import Router
from fluentogram import TranslatorRunner

from src.callbacks.WeatherCallback import WeatherCallback

from src.services.WeatherService import WeatherService

from src.keyboards import get_btns_weather
from src.keyboards import get_btns_weather_now
from src.keyboards import get_btns_start

from src.core.Logging import get_logger


router = Router()
_lg = get_logger()


# обработка нажатия кнопки Погода
@router.callback_query(WeatherCallback.filter())
async def weather_callback_handler(
    callback: CallbackQuery, callback_data: WeatherCallback, locale: TranslatorRunner
):

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
            text=locale.message_weather_menu(),
            reply_markup=get_btns_weather(user.id, locale),
        )

    # 🌡 Сейчас
    if callback_data.action == "weather_now":

        # TODO сделать переделать
        # # Проверить наличие локации в файле
        # if not user_data_service.user_has_location(user.id):
        #     await message.answer(
        #         get_message("RU_LN")["location_m"]["message_loc_not_post"]
        #     )
        #     return

        # # ✅ Проверить есть ли NULL значения
        # if user_data_service._has_null_location(user.id):
        #     _lg.info(
        #         f"Found NULL values in location for user {user.id}, attempting to fix..."
        #     )

        #     # Пытаемся исправить
        #     if user_data_service._fix_null_location(user.id):
        #         _lg.info(f"Successfully fixed NULL location for user {user.id}")
        #     else:
        #         _lg.warning(f"Could not fix NULL location for user {user.id}")

        #         await message.answer(
        #             text=get_message("RU_LN")["location_m"]["message_null_error"]
        #             + "\n"
        #             + get_message("RU_LN")["device_m"]["message"],
        #             reply_markup=get_btns_device(),
        #         )
        #         return

        # wn_all_ser_dict = WeatherService().get_weather_now(user.id) or {}

        # _lg.debug(f"ALL INFO weather now ser - {wn_all_ser_dict}")

        # day_or_night_emoji = (
        #     get_message("RU_LN")["weather_now_m"]["day_or_night_emoji"][0]
        #     if bool(wn_all_ser_dict["OpenMeteo"]["current"]["is_day"])
        #     else get_message("RU_LN")["weather_now_m"]["day_or_night_emoji"][1]
        # )

        # wnm = (
        #     # Header
        #     get_message("RU_LN")["weather_now_m"]["message_header"]
        #     .replace("{city}", user_data_service.get_usr_one_loc_par(user.id, "city"))
        #     .replace("{time}", wn_all_ser_dict["OpenMeteo"]["current"]["time"][11:])
        #     .replace("{day_or_night_emoji}", day_or_night_emoji)
        #     + "\n"
        #     + "\n"
        #     # Average 2
        #     + get_message("RU_LN")["weather_now_m"]["message_average"]
        #     + "\n"
        #     + get_message("RU_LN")["weather_now_m"]["message_average_filtered"]
        #     + "\n"
        #     # Title
        #     + get_message("RU_LN")["weather_now_m"]["message_section_title"]
        #     + "\n"
        # )

        wnm = "FIX USER"

        await message.edit_text(text=wnm, reply_markup=get_btns_weather_now())

    # 📊 Почасовой
    if callback_data.action == "weather_hours":
        await message.edit_text(
            text=locale.message_service_in_development(),
            reply_markup=get_btns_weather_now(),
        )
        await WeatherService.get_weather_hours()

    # 📆 На 5 дней
    if callback_data.action == "weather_5d":
        await message.edit_text(
            text=locale.message_service_in_development(),
            reply_markup=get_btns_weather_now(),
        )
        await WeatherService.get_weather_5d()

    # 🌅 Утро / 🌇 Вечер
    if callback_data.action == "weather_day_night":
        await message.edit_text(
            text=locale.message_service_in_development(),
            reply_markup=get_btns_weather_now(),
        )
        await WeatherService.get_weather_day_night()

    # 🌦 Осадки
    if callback_data.action == "weather_rain":
        await message.edit_text(
            text=locale.message_service_in_development(),
            reply_markup=get_btns_weather_now(),
        )
        await WeatherService.get_weather_rain()

    # 🧭 Ветер/давление
    if callback_data.action == "weather_wind_pressure":
        await message.edit_text(
            text=locale.message_service_in_development(),
            reply_markup=get_btns_weather_now(),
        )
        await WeatherService.get_weather_wind_pressure()

    # ⚙️ Настроить
    if callback_data.action == "weather_settings":
        await message.edit_text(
            text=locale.message_service_in_development(),
            reply_markup=get_btns_weather_now(),
        )

    # Функции на потом
    # 🔔 Подписка
    if callback_data.action == "weather_subscription":
        await message.edit_text(
            text=locale.message_service_in_development(),
            reply_markup=get_btns_weather_now(),
        )

    # 📍 Локация:
    if callback_data.action == "weather_location":

        # TODO СДЕЛАТЬ ЮЗЕР СЕРВИС
        # TODO сделать так чтобы не писало новое сообщение а изменялось меню на это
        # TODO сделать чтобы после взаимодействия с меню локации оно заменялось обратно на погодное

        # if not user_data_service.user_has_location(user.id):
        #     # Переброс на выбор платформы для определения местоположения
        #     await message.answer(
        #         text=get_message("RU_LN")["device_m"]["message"],
        #         reply_markup=get_btns_device(),
        #     )
        # else:
        #     # ✅ Проверяем есть ли NULL значения
        #     if user_data_service._has_null_location(user.id):
        #         _lg.info(f"Found NULL values in location for user {user.id}")

        #         await message.answer(
        #             text=get_message("RU_LN")["location_m"]["message_null_error"]
        #             + "\n"
        #             + get_message("RU_LN")["device_m"]["message"],
        #             reply_markup=get_btns_device(),
        #         )
        #     else:
        #         # Показать сохраненную локацию
        #         # location_display = user_data_service.format_user_location(user.id)

        location_display = "FIX USER"

        await message.answer(
            text=location_display,
        )

    # 🔙 Назад
    if callback_data.action == "weather_get_back":

        full_name_user = callback.from_user.full_name

        main_menu_text = f"{locale.message_start_hello()}{full_name_user or 'Пользователь'}{locale.message_start_main_menu()}"
        _lg.debug(f"{main_menu_text}")

        await message.edit_text(
            text=main_menu_text,
            reply_markup=get_btns_start(locale),
        )
