from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.storage.memory import MemoryStorage

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator
from fluentogram.exceptions import (
    KeyNotFoundError,
    FormatError,
    RootTranslatorNotFoundError,
)

from src.middlewares.middlewares import TranslateMiddleware, DataBaseMiddleware
from src.handlers import router as main_router

from src.utils import (
    settings,
    start_tuna,
    get_database_methods,
)
from bot.src.database.core import SessionLocal

import logging
from src.core import get_logger


storage = MemoryStorage()

_lg = get_logger()
_lg.debug("Logger init.")

# Get Telegram bot Token
TOKEN = settings.TELEGRAM_BOT_TOKEN

# Webserver settings
# For Docker, use localhost to bind to all interfaces
WEB_SERVER_HOST = "localhost"
WEB_SERVER_PORT = 8080

# Telegram webhook settings:
# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = "/webhook"
# Secret key to validate requests from Telegram (optional)
WEBHOOK_SECRET = "my-secret"

# Redirect for global net:
BASE_WEBHOOK_URL, process = start_tuna(WEB_SERVER_PORT)


def create_translator_hub() -> TranslatorHub | None:
    try:
        _lg.debug("Creating a TranslatorHub.")

        t_hub = TranslatorHub(
            {"ru": ("ru",)},
            translators=[
                FluentTranslator(
                    "ru",
                    translator=FluentBundle.from_files(
                        "ru-RU",
                        filenames=[
                            "bot/src/i18n/ru/text.ftl",
                            "bot/src/i18n/ru/button.ftl",
                        ],
                    ),
                )
            ],
            root_locale="ru",
        )

        _lg.info("TranslatorHub created successfully.")
        return t_hub

    except KeyNotFoundError as e:
        _lg.critical(f"Translation key not found: {e.key}")
    except RootTranslatorNotFoundError as e:
        _lg.critical(f"Root locale translator missing: {e.root_locale}")
    except FormatError as e:
        _lg.critical(f"Formatting error for key {e.key}: {e.original_error}")
    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


def create_dispatcher(db) -> Dispatcher | None:
    """
    Create and configure Dispatcher with routers

    Returns:
        Dispatcher | None: Configured dispatcher or None if error
    """
    try:
        _lg.debug("Create Dispatcher.")

        t_hub = create_translator_hub()
        if not t_hub:
            _lg.critical("Failed to create TranslatorHub")
            return None

        dp = Dispatcher(storage=storage, t_hub=t_hub)

        dp.include_router(main_router)

        dp.message.middleware(TranslateMiddleware())
        dp.message.outer_middleware(DataBaseMiddleware(db=db))

        dp.callback_query.middleware(TranslateMiddleware())
        dp.callback_query.outer_middleware(DataBaseMiddleware(db=db))

        _lg.info("Dispatcher created successfully.")
        return dp

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


async def on_startup_set_webhook(bot: Bot) -> None:
    """Set webhook on startup"""
    try:
        webhook_url = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
        _lg.info(f"Setting webhook to: {webhook_url}")

        await bot.delete_webhook(drop_pending_updates=True)
        _lg.info("Old webhook deleted")

        result = await bot.set_webhook(
            url=webhook_url,
            secret_token=WEBHOOK_SECRET,
            allowed_updates=["message", "callback_query"],
        )

        _lg.info(f"Webhook set result: {result}")

        webhook_info = await bot.get_webhook_info()
        _lg.info(f"Current webhook: {webhook_info.url}")
        _lg.info(f"Allowed updates: {webhook_info.allowed_updates}")

    except Exception as e:
        _lg.critical(f"Failed to set webhook: {e}")


def create_bot() -> Bot | None:
    """
    Create and configure Telegram bot

    Returns:
        Bot | None: Configured bot instance or None if error
    """
    try:
        _lg.debug("Creating bot.")

        if not TOKEN:
            _lg.critical("Token is empty or invalid.")
            return None

        bot = Bot(
            token=TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        _lg.info("Bot created successfully.")
        return bot

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")
        return None


def main() -> None:
    """Main bot execution function"""
    try:
        _lg.debug("Start main func.")

        bot = create_bot()
        if bot is None:
            _lg.critical("Failed to create a bot. Exiting.")
            return

        dp = create_dispatcher(get_database_methods(SessionLocal))
        if dp is None:
            _lg.critical("Failed to create a dispatcher. Exiting.")
            return

        dp.startup.register(on_startup_set_webhook)

        # Вместо полинга вебхуки
        # Создание aiohttp Application
        app = web.Application()

        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET,
        )

        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        # Mount dispatcher startup and shutdown hooks to aiohttp application
        setup_application(app, dp, bot=bot)

        # And finally start webserver
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

    except KeyboardInterrupt:
        _lg.info("Bot stopped by user (KeyboardInterrupt).")
    except Exception as e:
        _lg.critical(f"Internal error: {e}.")
    finally:
        _lg.info("Tuna tunnel stopping...")
        process.terminate()
        process.wait()
        _lg.info("Tuna tunnel stopped.")
        _lg.info("Bot stopped.")
        _lg.info("Logging stopped.")
        logging.shutdown()


if __name__ == "__main__":
    main()
