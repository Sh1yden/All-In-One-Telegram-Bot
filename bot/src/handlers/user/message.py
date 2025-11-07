from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message, User
from fluentogram import TranslatorRunner

from src.keyboards import get_btns_start
from src.keyboards import get_btns_weather

from src.core import get_logger


router = Router()
_lg = get_logger()


@router.message(Command("start"))
async def command_start_handler(message: Message, locale: TranslatorRunner) -> None:
    """Handle /start command and display welcome message"""
    try:
        _lg.debug("Start handler activated.")

        if message.from_user is None:
            _lg.warning("User is None in start handler")
            await message.answer(locale.message_service_error_not_user_enable())
            return

        full_name_user = html.bold(message.from_user.full_name)
        _lg.debug(f"User: {full_name_user}")

        main_menu_text = f"{locale.message_start_hello()}{full_name_user or 'Пользователь'}{locale.message_start_main_menu()}"
        _lg.debug("Main menu text prepared.")

        await message.answer(
            text=main_menu_text,
            reply_markup=get_btns_start(locale),
        )

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


# обработка команды /weatherMenu
@router.message(Command("weatherMenu"))
async def command_weather_handler(message: Message, locale: TranslatorRunner) -> None:

    user: User | None = message.from_user

    await message.answer(
        text=locale.message_weather_menu(),
        reply_markup=get_btns_weather(user.id, locale),
    )
