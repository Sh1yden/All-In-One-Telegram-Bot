from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_inl_btns_start() -> InlineKeyboardMarkup:
    """Кнопки снизу сообщения после команды /start."""

    builder = InlineKeyboardBuilder()

    # добавить еще кнопок для других функций
    builder.row(InlineKeyboardButton(text="Погода", callback_data="/weather"))

    return builder.as_markup()
