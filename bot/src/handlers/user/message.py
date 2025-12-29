from typing import Any, Dict

from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message, User
from fluentogram import TranslatorRunner

from src.core import get_logger
from src.keyboards import (
    get_btns_device,
    get_btns_start,
    get_btns_weather,
    get_btns_weather_now,
)
from src.services import get_weather_now

router = Router()
_lg = get_logger()


# обработка команды /start
@router.message(Command("start"))
async def command_start_handler(
    message: Message,
    locale: TranslatorRunner,
    repos: Dict[str, Any],
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
        user_repo = repos["user_repo"]
        if not user_repo.exists(user.id):
            user_repo.save_from_telegram_user(user)
            _lg.debug(f"New user created: {user.id}")

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


# обработка команды /help
@router.message(Command("help"))
async def command_help_handler(message: Message, locale: TranslatorRunner):
    """Handle /help command"""
    await message.answer(
        text=locale.message_help(),
        reply_markup=None,
    )


# обработка команды /weatherMenu
@router.message(Command("weatherMenu"))
async def command_weather_handler(
    message: Message,
    locale: TranslatorRunner,
    repos: Dict[str, Any],
) -> None:
    """Handle /weatherMenu command"""
    user: User | None = message.from_user
    user_repo = repos["user_repo"]

    if user is None:
        _lg.warning("User is None")
        await message.answer(locale.message_service_error_not_user_enable())
        return

    await message.answer(
        text=locale.message_weather_menu(),
        reply_markup=get_btns_weather(
            user_id=user.id, locale=locale, user_repo=user_repo
        ),
    )


# обработка команды /weatherNow
@router.message(Command("weatherNow"))
async def command_weather_now_handler(
    message: Message,
    locale: TranslatorRunner,
    repos: Dict[str, Any],
):
    """Handle /weatherNow command"""
    user: User | None = message.from_user
    user_repo = repos["user_repo"]
    weather_repo = repos["weather_repo"]

    if user is None:
        _lg.warning("User is None")
        await message.answer(locale.message_service_error_not_user_enable())
        return

    if user_repo.has_location(user.id):
        location = user_repo.get_by_id(user.id)
        latitude = location.get("latitude", None)
        longitude = location.get("longitude", None)
        city = location.get("city")

        all_msg = await get_weather_now(
            locale=locale,
            weather_repo=weather_repo,
            city=city,
            latitude=latitude,
            longitude=longitude,
            usr_loc=location,
        )

        _lg.debug(f"all_msg is - {all_msg}")

        await message.answer(
            text=str(all_msg), reply_markup=get_btns_weather_now(locale)
        )
    else:
        await message.answer(
            text=locale.message_location_not_posted(),
            reply_markup=get_btns_weather_now(locale),
        )


# обработка команды /location
@router.message(Command("location"))
async def request_location(
    message: Message,
    locale: TranslatorRunner,
    repos: Dict[str, Any],
) -> None:
    """Handle /location command"""
    user: User | None = message.from_user
    user_repo = repos["user_repo"]

    if user is None:
        _lg.warning("User is None")
        await message.answer(locale.message_service_error_not_user_enable())
        return

    if user_repo.has_location(user.id):
        location = user_repo.get_by_id(user.id)

        city = location.get("city")
        latitude = location.get("latitude")
        longitude = location.get("longitude")

        await message.answer(
            text=locale.message_location_good_send(
                city=city,
                latitude=latitude,
                longitude=longitude,
            ),
            reply_markup=get_btns_weather_now(locale),
        )
    else:
        await message.answer(
            text=locale.message_device_select(),
            reply_markup=get_btns_device(locale),
        )


# обработка команды /device
@router.message(Command("device"))
async def command_device_handler(message: Message, locale: TranslatorRunner):
    """Handle /device command"""
    await message.answer(
        text=locale.message_device_select(),
        reply_markup=get_btns_device(locale),
    )
