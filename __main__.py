import asyncio
import logging
import json

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.handlers.start import router as start_router
from src.handlers.weather import router as weather_router

# from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger

lg = get_logger()


def get_token():

    try:
        lg.debug("Getting token.")

        with open(
            "c:\\Users\\Shayden\\Documents\\All Code Programming\\GitHub\\_secret_api_keys\\api_keys.json",
            "r",
            encoding="utf-8",
        ) as f:
            data = json.load(f)

            if data["AIO_BOT_TOKEN"]:
                lg.debug("Getting token successful.")

            return data["AIO_BOT_TOKEN"]
    except Exception as e:
        lg.critical(f"Internal error: {e}.")


def create_bot() -> Bot | None:
    try:
        lg.debug("Creating bot.")

        bot = Bot(
            token=get_token(), default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        return bot
    except Exception as e:
        lg.critical(f"Internal error: {e}.")


def create_dispatcher() -> Dispatcher | None:
    try:
        lg.debug("Create Dispatcher.")
        dp = Dispatcher()

        dp.include_router(start_router)
        dp.include_router(weather_router)

        return dp
    except Exception as e:
        lg.critical(f"Internal error:{e}.")


async def main():
    try:
        lg.debug("Start main func")
        bot = create_bot()
        dp = create_dispatcher()

        await dp.start_polling(bot)
    except Exception as e:
        lg.critical(f"Internal error:{e}.")


if __name__ == "__main__":
    asyncio.run(main())
