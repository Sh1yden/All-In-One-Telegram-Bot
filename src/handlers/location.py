from aiogram.types import Message, User
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router

from aiogram import F
from aiogram.types import Location, ReplyKeyboardRemove

from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger
from src.services.UserDataService import user_data_service

from src.services.GeocodingOMAPI import get_cord_from_city
from src.services.NominatimAPI import get_city_from_cord

from src.states.LocationState import LocationState
from src.utils.state_helpers import clear_state

from src.keyboards.k_device import get_inl_btns_device
from src.config.TextMessages import get_message


router = Router()
_appcfg = AppConfig()
_lg = get_logger()


# Ответ на команду
@router.message(Command("location"))
async def request_location(message: Message):

    # TODO копия кода с weather callback'a - weather_location понять как не копировать код и переделать

    user: User | None = message.from_user

    if not user_data_service.user_has_location(user.id):
        # Переброс на выбор платформы для определения местоположения
        await message.answer(
            text=get_message("RU_LN")["device_m"]["message"],
            reply_markup=get_inl_btns_device(),
        )
    else:
        # ✅ Проверяем есть ли NULL значения
        if user_data_service._has_null_location(user.id):
            _lg.info(f"Found NULL values in location for user {user.id}")

            await message.answer(
                text=get_message("RU_LN")["location_m"]["message_null_error"]
                + "\n"
                + get_message("RU_LN")["device_m"]["message"],
                reply_markup=get_inl_btns_device(),
            )
        else:
            # Показать сохраненную локацию
            location_display = user_data_service.format_user_location(user.id)
            await message.answer(
                text=location_display,
            )


# Ответ на отправку геолокации только с ТЕЛЕФОНА
@router.message(LocationState.waiting_for_city_phone, F.location)
async def handle_location_phone(message: Message, state: FSMContext):
    try:
        _lg.debug("Start handle location on phone.")
        location_phone: Location | None = message.location
        user: User | None = message.from_user

        if not location_phone:
            await message.answer(get_message("RU_LN")["location_m"]["message_error"])
            await clear_state(state)
            return

        lat = location_phone.latitude
        lon = location_phone.longitude
        city = get_city_from_cord(lat, lon, user_agent="TestApp/1.0")
        _lg.debug(f"User city on phone is - {city}.")

        # Сохранить данные в файл
        success = user_data_service.save_user_location(
            user_id=user.id,
            username=user.username or "",
            full_name=user.full_name or "Unknown",
            location_type="phone",
            city=city,
            latitude=lat,
            longitude=lon,
        )

        if success:
            await message.answer(
                f"{get_message("RU_LN")["location_m"]["message_good_loc_w_phone"]}{lat}{get_message("RU_LN")["location_m"]["message_good_loc_l_phone"]}{lon}",
                reply_markup=ReplyKeyboardRemove(),  # убираем клавиатуру
            )
        else:
            await message.answer(get_message("RU_LN")["location_m"]["message_error"])

        # Очистить состояние
        await clear_state(state)
    except Exception as e:
        _lg.error(f"Internal error: {e}.")


# Ответ на отправку геолокации только с ПК
@router.message(LocationState.waiting_for_city_pc, F.text)
async def handle_location_pc(message: Message, state: FSMContext):
    try:
        _lg.debug("Start handle location on PC.")

        location_pc = message.text
        user: User | None = message.from_user

        # Проверить, что это не команда отмены
        if location_pc == get_message("RU_LN")["location_m"]["buttons"][1]:
            await clear_state(state)
            await message.answer(
                text=get_message("RU_LN")["location_m"]["message_cancel"]
            )
            return

        cord = get_cord_from_city(location_pc) or {}
        city = get_city_from_cord(cord["lat"], cord["lon"], user_agent="TestApp/1.0")
        _lg.debug(f"User city on pc is - {city}.")

        # Сохранить данные в файл
        success = user_data_service.save_user_location(
            user_id=user.id,
            username=user.username or "",
            full_name=user.full_name or "Unknown",
            location_type="pc",
            city=city,
            latitude=cord["lat"],
            longitude=cord["lon"],
        )

        if success:
            await message.answer(
                text=get_message("RU_LN")["location_m"]["message_good_loc_city_pc"]
                + location_pc
            )
        else:
            await message.answer(get_message("RU_LN")["location_m"]["message_error"])

        # Очистить состояние
        await clear_state(state)
    except Exception as e:
        _lg.error(f"Internal error: {e}.")


# Обработка отмены
@router.message(
    LocationState.waiting_for_city_phone,
    F.text == get_message("RU_LN")["location_m"]["buttons"][1],
)
@router.message(
    LocationState.waiting_for_city_pc,
    F.text == get_message("RU_LN")["location_m"]["buttons"][1],
)
async def handle_cancel_location(message: Message, state: FSMContext):
    await clear_state(state)
    await message.answer(
        get_message("RU_LN")["location_m"]["message_cancel"],
        reply_markup=ReplyKeyboardRemove(),
    )
