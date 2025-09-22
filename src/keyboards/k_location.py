from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.config.TextMessages import get_message


def get_inl_btns_location() -> ReplyKeyboardMarkup:

    builder = ReplyKeyboardBuilder()

    builder.button(
        text=get_message("RU_LN")["location_m"]["buttons"][0],
        request_location=True,  # запрос локации через тг
    )

    builder.button(text=get_message("RU_LN")["location_m"]["buttons"][1])

    builder.adjust(1)  # одна кнопка в строке
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
