from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message, User
from fluentogram import TranslatorRunner

from bot.src.utils.db_utils import MethodsOfDatabase
from bot.src.database.models import UserAllInfo

from src.keyboards import (
    get_btns_start,
    get_btns_weather,
    get_btns_weather_now,
    get_btns_device,
)

from src.core import get_logger


router = Router()
_lg = get_logger()


# обработка команды /start
@router.message(Command("start"))
async def command_start_handler(
    message: Message, locale: TranslatorRunner, db: MethodsOfDatabase
) -> None:
    """Handle /start command and display welcome message"""
    try:
        _lg.debug("Start handler activated.")

        user: User | None = message.from_user

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

        # Создание пользователя в БД
        if not db.user_exists(UserAllInfo, user.id):
            success, msg = db.create_one_user(
                model=UserAllInfo,
                user=user,
            )
            if success:
                _lg.debug(f"New user created: {user.id}")
            else:
                _lg.error(f"Failed to create user: {msg}")

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


# обработка команды /help
@router.message(Command("help"))
async def command_help_handler(message: Message, locale: TranslatorRunner):

    await message.answer(
        text=locale.message_help(),
        reply_markup=None,
    )


# обработка команды /weatherMenu
@router.message(Command("weatherMenu"))
async def command_weather_handler(message: Message, locale: TranslatorRunner) -> None:

    user: User | None = message.from_user

    await message.answer(
        text=locale.message_weather_menu(),
        reply_markup=get_btns_weather(user.id, locale),
    )


# обработка команды /weatherNow
@router.message(Command("weatherNow"))
async def command_weather_now_handler(message: Message, locale: TranslatorRunner):

    user: User | None = message.from_user

    # TODO сделать ответ на команду

    await message.answer(
        text="Заглушка при открытии через команду",  # ! заглушка
        reply_markup=get_btns_weather_now(locale),
    )


# обработка команды /location
@router.message(Command("location"))
async def request_location(message: Message, locale: TranslatorRunner) -> None:
    """Handle /location command"""
    user: User | None = message.from_user

    if user is None:
        _lg.warning("User is None in request_location")
        await message.answer(locale.message_service_error_not_user_enable())
        return

    # TODO await _check_and_display_location(message, user.id)


# обработка команды /device
@router.message(Command("device"))
async def command_device_handler(message: Message, locale: TranslatorRunner):

    await message.answer(
        text=locale.message_device_select(),
        reply_markup=get_btns_device(locale),
    )
