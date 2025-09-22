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


# Ответ на отправку геолокации
@router.message(F.location)
async def handle_location(message: Message):
    location: Location = message.location
    lat = location.latitude
    lon = location.longitude

    await message.answer(
        f"{get_message("RU_LN")["location_m"]["message2"]}{lat}{get_message("RU_LN")["location_m"]["message3"]}{lon}",
        reply_markup=ReplyKeyboardRemove(),  # убираем клавиатуру
    )

    # Теперь можно передать координаты в WeatherService и т.п.
    # weather = await WeatherService.get_weather_by_coords(lat, lon)
