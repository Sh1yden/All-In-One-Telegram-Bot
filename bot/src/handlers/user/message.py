from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, html

router = Router()

# _lg = logging  # ! заглушка


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handle /start command and display welcome message"""
    try:
        await message.answer(text="First Start")
        # _lg.debug("Start handler activated.")

        # if message.from_user is None:
        #     _lg.warning("User is None in start handler")
        #     await message.answer(
        #         get_message("RU_LN")["service_m"]["message_error_not_user_enable"]
        #     )
        #     return

        # full_name_user = html.bold(message.from_user.full_name)
        # _lg.debug(f"User: {full_name_user}")

        # main_menu_text = (
        #     f"{get_message('RU_LN')['start_m']['message_hello']}"
        #     f"{full_name_user or 'Пользователь'}"
        #     f"{get_message('RU_LN')['start_m']['message_main_menu']}"
        # )
        # _lg.debug("Main menu text prepared.")

        # await message.answer(
        #     text=main_menu_text,
        #     reply_markup=get_inl_btns_start(),
        # )

    except Exception as e:
        # _lg.critical(f"Internal error: {e}.")
        return
