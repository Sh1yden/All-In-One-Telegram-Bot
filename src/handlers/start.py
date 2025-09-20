from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, html

from src.keyboards.k_start import get_inl_btns_start
from src.core.Logging import get_logger
from src.config.TextMessages import get_message


router = Router()
_lg = get_logger()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Вывод приветственного сообщения после команды /start"""
    try:
        _lg.debug("Start handler.")

        full_name_user = html.bold(message.from_user.full_name)
        _lg.debug(f"{full_name_user}")

        main_menu_text = f"""{get_message("RU_LN")["start_m"]["message1"]}{full_name_user or "Пользователь"}{get_message("RU_LN")["start_m"]["message2"]}"""
        _lg.debug(f"{main_menu_text}")

        await message.answer(
            text=main_menu_text,
            reply_markup=get_inl_btns_start(),
        )

    except Exception as e:
        _lg.critical(f"Internal error:{e}.")
