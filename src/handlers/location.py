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

from src.keyboards.k_location import get_inl_btns_location
from src.config.TextMessages import get_message


router = Router()
_appcfg = AppConfig()
_lg = get_logger()


# Ответ на команду
@router.message(Command("location"))
async def request_location(message: Message):
    # TODO разделить на телефон и пк

    await message.answer(
        get_message("RU_LN")["location_m"]["message_send_loc_phone"],
        reply_markup=get_inl_btns_location(),
    )


# Ответ на отправку геолокации только с ТЕЛЕФОНА
@router.message(LocationState.waiting_for_city_phone, F.location)
async def handle_location_phone(message: Message, state: FSMContext):
    try:
        _lg.debug("Start handle location on phone.")
        location_phone: Location | None = message.location
        user: User | None = message.from_user

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
        _lg.debug("Start handle location on phone.")

        location_pc = message.text
        user: User | None = message.from_user

        # Проверить, что это не команда отмены
        if location_pc == "❌ Отмена":
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
@router.message(LocationState.waiting_for_city_phone, F.text == "❌ Отмена")
@router.message(LocationState.waiting_for_city_pc, F.text == "❌ Отмена")
async def handle_cancel_location(message: Message, state: FSMContext):
    await clear_state(state)
    await message.answer(
        get_message("RU_LN")["location_m"]["message_cancel"],
        reply_markup=ReplyKeyboardRemove(),
    )
