from aiogram import Router, Bot, html
from aiogram.filters import Command
from aiogram.types import Message

from fluentogram import TranslatorRunner

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
            await message.answer(locale.message_error_not_user_enable())
            return

        full_name_user = html.bold(message.from_user.full_name)
        _lg.debug(f"User: {full_name_user}")

        main_menu_text = f"""
            {locale.message_hello()}{full_name_user or 'Пользователь'}{locale.message_main_menu()}
        """
        _lg.debug("Main menu text prepared.")

        await message.answer(
            text=main_menu_text,
            # reply_markup=get_inl_btns_start(),
        )

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")
