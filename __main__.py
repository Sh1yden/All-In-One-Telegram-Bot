import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.handlers.start import router as start_router
from src.handlers.help import router as help_router
from src.handlers.weather import router as weather_router
from src.handlers.location import router as location_router
from src.handlers.device import router as device_router

# from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger
from src.config.Token import get_token


# _appcfg = AppConfig()

_lg = get_logger()
_lg.debug("Logger init.")

__TOKEN_PATH = os.path.expanduser(
    "~\\Documents\\All Code Programming\\_secret_api_keys\\api_keys.json"
)


def create_bot() -> Bot | None:
    try:
        _lg.debug("Creating bot.")

        bot = Bot(
            token=get_token(__TOKEN_PATH),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        return bot

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


def create_dispatcher() -> Dispatcher | None:
    try:
        _lg.debug("Create Dispatcher.")
        dp = Dispatcher()

        dp.include_router(start_router)
        dp.include_router(help_router)
        dp.include_router(weather_router)
        dp.include_router(location_router)
        dp.include_router(device_router)

        return dp

    except Exception as e:
        _lg.critical(f"Internal error:{e}.")


async def main():
    try:
        _lg.debug("Start main func.")

        bot = create_bot()
        if bot is None:
            _lg.critical("Failed to create a bot. Exiting.")
            return

        dp = create_dispatcher()
        if dp is None:
            _lg.critical("Failed to create a dispatcher. Exiting.")
            return

        await dp.start_polling(bot)

    except Exception as e:
        _lg.critical(f"Internal error:{e}.")


if __name__ == "__main__":
    asyncio.run(main())
