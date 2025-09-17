from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram import Router, html


router = Router()


# обработка нажатия кнопки Погода
# @router.callback_query(CallbackData, "weather")
# async def weather_callback(callback: CallbackQuery):

#     await callback.answer("Получаю погоду...")


# обработка команды /weather
@router.message(Command("weather"))
async def command_weather_handler(message: Message):

    await message.answer("Получаю погоду...")
