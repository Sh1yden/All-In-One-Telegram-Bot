from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, html

from src.keyboards.k_start import get_inl_btns_start


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Вывод приветственного сообщения после команды /start"""

    full_name_user = html.bold(message.from_user.full_name)
    main_menu_text = f"""
Привет, {full_name_user or "Пользователь"}!  Тут будет меню выбора различных функций бота. Так же чтобы вывести все команды бота напиши /help. Вызвать функцию погоды можно нажав кнопку ниже, либо же введя команду /weather_menu.
        """

    await message.answer(
        text=main_menu_text,
        reply_markup=get_inl_btns_start(),
    )
