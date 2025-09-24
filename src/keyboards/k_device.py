from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.callbacks.DeviceCallback import DeviceCallback
from src.config.TextMessages import get_message


def get_inl_btns_device() -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_message("RU_LN")["device_m"]["buttons"][0],
            callback_data=DeviceCallback(action="device_phone").pack(),
        ),
        InlineKeyboardButton(
            text=get_message("RU_LN")["device_m"]["buttons"][1],
            callback_data=DeviceCallback(action="device_pc").pack(),
        ),
    )

    return builder.as_markup(resize_keyboard=True)
