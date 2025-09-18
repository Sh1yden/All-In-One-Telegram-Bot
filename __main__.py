import asyncio
import logging
import json

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.handlers.start import router as start_router
from src.handlers.weather import router as weather_router


def get_token():

    with open(
        "c:\\Users\\Shayden\\Documents\\All Code Programming\\GitHub\\_secret_api_keys\\api_keys.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
        return data["AIO_BOT_TOKEN"]


def create_bot() -> Bot:

    bot = Bot(
        token=get_token(), default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    return bot


def create_dispatcher() -> Dispatcher:

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(weather_router)

    return dp


async def main():

    bot = create_bot()
    dp = create_dispatcher()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
