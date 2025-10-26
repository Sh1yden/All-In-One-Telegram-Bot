import asyncio
import os
import logging
from dotenv import load_dotenv

load_dotenv()

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers import router as main_router


# Get Telegram bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Webserver settings
# For Docker, use 0.0.0.0 to bind to all interfaces
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 8080

# Telegram webhook settings:
# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = "/webhook"
# Secret key to validate requests from Telegram (optional)
WEBHOOK_SECRET = "my-secret"

# Redirect for global net:
BASE_WEBHOOK_URL = os.getenv("TUNA_TUNNEL_URL")  # ! Менять при каждом запуске в .env

storage = MemoryStorage()

_lg = logging.getLogger()
_lg.debug("Logger init.")


def create_bot() -> Bot | None:
    """
    Create and configure Telegram bot

    Returns:
        Bot | None: Configured bot instance or None if error
    """
    try:
        _lg.debug("Creating bot.")

        token = TOKEN

        if not token:
            _lg.critical("Token is empty or invalid")
            return None

        bot = Bot(
            token=token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        _lg.debug("Bot created successfully.")
        return bot

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")
        return None


def create_dispatcher() -> Dispatcher | None:
    """
    Create and configure Dispatcher with routers

    Returns:
        Dispatcher | None: Configured dispatcher or None if error
    """
    try:
        _lg.debug("Create Dispatcher.")

        # All handlers should be attached to the Router (or Dispatcher)
        dp = Dispatcher(storage=storage)

        dp.include_router(main_router)

        _lg.debug("Dispatcher created successfully.")
        return dp

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")
        return None


async def on_startup_set_webhook(bot: Bot) -> None:
    # If you have a self-signed SSL certificate, then you will need to send a public
    # certificate to Telegram
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET
    )


async def main() -> None:
    """Main bot execution function"""
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
        # Register startup hook to initialize webhook
        dp.startup.register(on_startup_set_webhook)

        # Вместо полинга вебхуки
        # Создание aiohttp Application
        app = web.Application()

        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET,
        )
        # Register webhook handler on application
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        # Mount dispatcher startup and shutdown hooks to aiohttp application
        setup_application(app, dp, bot=bot)

        # And finally start webserver
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

    except KeyboardInterrupt:
        _lg.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        _lg.critical(f"Internal error: {e}.")
    finally:
        _lg.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
