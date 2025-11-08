from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from fluentogram import TranslatorRunner


def get_btns_location(locale: TranslatorRunner) -> ReplyKeyboardMarkup:

    builder = ReplyKeyboardBuilder()

    # 📍 Отправить местоположение
    builder.button(
        text=locale.button_location_send(),
        request_location=True,  # запрос локации через тг
    )

    # ❌ Отмена
    builder.button(text=locale.button_location_cancel())

    builder.adjust(1)  # одна кнопка в строке
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
