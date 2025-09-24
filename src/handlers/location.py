from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from aiogram import F
from aiogram.types import Location, ReplyKeyboardRemove

from src.keyboards.k_location import get_inl_btns_location
from src.config.TextMessages import get_message


router = Router()


# Ответ на команду
@router.message(Command("location"))
async def request_location(message: Message):

    await message.answer(
        get_message("RU_LN")["location_m"]["message1"],
        reply_markup=get_inl_btns_location(),
    )


# Ответ на отправку геолокации только с телефона
@router.message(F.location)
async def handle_location_phone(message: Message):

    location_phone: Location | None = message.location

    lat = location_phone.latitude
    lon = location_phone.longitude

    await message.answer(
        f"{get_message("RU_LN")["location_m"]["message2"]}{lat}{get_message("RU_LN")["location_m"]["message3"]}{lon}",
        reply_markup=ReplyKeyboardRemove(),  # убираем клавиатуру
    )

    # Теперь можно передать координаты
    # weather = await GeocodingOMAPI.get_location_phone(lat, lon)


@router.message(F.text)
async def handle_location_pc(message: Message):

    location_pc = message.text

    await message.answer(
        text=get_message("RU_LN")["location_m"]["message2pc"] + location_pc
    )

    # Передача города
    # weather = await GeocodingOMAPI.get_location_pc(location_pc)
