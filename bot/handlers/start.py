from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, html

from bot.keyboards.k_start import get_inl_btns_start


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Вывод приветственного сообщения после команды /start"""

    await message.answer(
        f"""
Привет, {html.bold(message.from_user.full_name) or "Пользователь"}!
Тут будет меню выбора различных функций бота. Так же чтобы вывести все команды бота напиши /help.
Вызвать функцию погоды можно нажав кнопку ниже, либо же введя команду /weather.
        """,
        reply_markup=get_inl_btns_start(),
    )
