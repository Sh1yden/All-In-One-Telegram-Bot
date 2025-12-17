import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub
from fluentogram.exceptions import (
    FormatError,
    KeyNotFoundError,
    RootTranslatorNotFoundError,
)
from src.core import get_logger, setup_logging
from src.database.core import SessionLocal
from src.database.repositories.factory import create_repositories
from src.handlers import router as main_router
from src.middlewares.middlewares import DataBaseMiddleware, TranslateMiddleware
from src.utils import settings, start_tuna

storage = MemoryStorage()

setup_logging(level="DEBUG")
_lg = get_logger(__name__)

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
WEBHOOK_SECRET = settings.TELEGRAM_WEBHOOK_SECRET

# Redirect for global net:
BASE_WEBHOOK_URL, tuna_process = start_tuna(WEB_SERVER_PORT)


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


def create_dispatcher(repos) -> Dispatcher | None:
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
        dp.message.outer_middleware(DataBaseMiddleware(repos=repos))

        dp.callback_query.middleware(TranslateMiddleware())
        dp.callback_query.outer_middleware(DataBaseMiddleware(repos=repos))

        _lg.info("Dispatcher created successfully.")
        return dp

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


async def on_startup_set_webhook(bot: Bot) -> None:
    """Set webhook on startup"""
    try:
        webhook_url = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
        _lg.debug(f"Setting webhook to: {webhook_url}")

        await bot.delete_webhook(drop_pending_updates=True)
        _lg.debug("Old webhook deleted")

        result = await bot.set_webhook(
            url=webhook_url,
            secret_token=WEBHOOK_SECRET,
            allowed_updates=["message", "callback_query"],
        )

        _lg.debug(f"Webhook set result: {result}")

        webhook_info = await bot.get_webhook_info()
        _lg.info(f"Current webhook: {webhook_info.url}")
        _lg.debug(f"Allowed updates: {webhook_info.allowed_updates}")

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


async def run_bot() -> None:
    """Async main app function."""
    repos = None
    try:
        _lg.debug("Start main func.")

        bot = create_bot()
        if bot is None:
            _lg.critical("Failed to create a bot. Exiting.")
            return

        repos = create_repositories(SessionLocal)
        _lg.info("Database initialized.")

        dp = create_dispatcher(repos)
        if dp is None:
            _lg.critical("Failed to create a dispatcher. Exiting.")
            return

        # Set webhook
        await on_startup_set_webhook(bot)

        # Setup web application
        app = web.Application()

        webhook_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET,
        )
        webhook_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)

        # Start web server
        runner = web.AppRunner(app)
        if runner is None:
            _lg.critical("Failed to create a runner. Exiting.")
            return
        await runner.setup()

        site = web.TCPSite(runner, WEB_SERVER_HOST, WEB_SERVER_PORT)
        await site.start()

        _lg.info(f"Web server started on {WEB_SERVER_HOST}:{WEB_SERVER_PORT}")
        _lg.info("Bot is running. Press Ctrl+C to stop.")

        await asyncio.Event().wait()

    except asyncio.CancelledError:
        _lg.info("Bot stopped by signal.")
    except KeyboardInterrupt:
        _lg.info("Bot stopped by user.")
    except Exception as e:
        _lg.critical(f"Critical error: {e}.", exc_info=True)
    finally:
        _lg.info("Starting cleanup:")

        # Cleanup
        # Stop web server
        if runner:  # type: ignore
            try:
                await runner.cleanup()
                _lg.info("Web server stopped.")
            except Exception as e:
                _lg.error(f"Error stopping web server: {e}.")

        # Delete webhook and close bot
        if bot:  # type: ignore
            try:
                await bot.delete_webhook(drop_pending_updates=False)
                _lg.info("Webhook deleted.")
            except Exception as e:
                _lg.error(f"Error deleting webhook: {e}.")

            try:
                await bot.session.close()
                _lg.info("Bot session closed.")
            except Exception as e:
                _lg.error(f"Error closing bot: {e}.")

        # Close storage
        try:
            await storage.close()
            _lg.info("Storage closed.")
        except Exception as e:
            _lg.error(f"Error closing storage: {e}.")

        # Close database
        if repos:  # type: ignore
            try:
                repos["user_repo"].db_methods.close()
                _lg.info("Database closed.")
            except Exception as e:
                _lg.error(f"Error closing database: {e}.")

        # Stop Tuna tunnel
        if tuna_process:
            try:
                _lg.debug("Stopping Tuna tunnel...")
                tuna_process.terminate()
                tuna_process.wait(timeout=3)
                _lg.info("Tuna tunnel stopped.")
            except Exception:
                try:
                    tuna_process.kill()
                    _lg.warning("Tuna tunnel killed.")
                except Exception as e:
                    _lg.error(f"Error killing Tuna: {e}.")

        _lg.info("Cleanup completed!")


def main() -> None:
    """Main point."""
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        _lg.info("Received Ctrl+C.")
    finally:
        _lg.info("Bot stopped.")
        _lg.info("Logging stopped.")
        logging.shutdown()


if __name__ == "__main__":
    main()
