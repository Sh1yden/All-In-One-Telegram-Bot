from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router

from src.callbacks.HelpCallback import HelpCallback
from src.handlers.start import command_start_handler
from src.core.Logging import get_logger
from src.config.TextMessages import get_message

router = Router()


@router.callback_query(HelpCallback.filter())
async def help_callback_handler(callback: CallbackQuery, callback_data: HelpCallback):
    pass


@router.message(Command("help"))
async def command_help_handler(message: Message):

    await message.answer(
        text=get_message("RU_LN")["help_m"]["message"],
        reply_markup=None,
    )
