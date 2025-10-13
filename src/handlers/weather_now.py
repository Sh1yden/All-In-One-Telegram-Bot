from aiogram.types import Message, User
from aiogram.filters import Command
from aiogram import Router

from src.keyboards.k_weather_now import get_inl_btns_weather_now  # BTN

from src.config.TextMessages import get_message

router = Router()


# обработка команды /weatherNow
@router.message(Command("weatherNow"))
async def command_weather_handler(message: Message):

    user: User | None = message.from_user

    # TODO сделать ответ на команду

    await message.answer(
        text="Заглушка при открытии через команду",  # ! заглушка
        reply_markup=get_inl_btns_weather_now(),
    )
