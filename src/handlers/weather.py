from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, html

from src.callbacks.WeatherCallback import WeatherCallback  # CALLBACK

# from services.WeatherService import WeatherService  # API # TODO

from src.keyboards.k_weather import get_inl_btns_weather  # BTN # TODO
from src.keyboards.k_start import get_inl_btns_start  # BTN # TODO
from src.core.Logging import get_logger
from src.config.TextMessages import get_message


router = Router()
_lg = get_logger()


# обработка нажатия кнопки Погода
@router.callback_query(WeatherCallback.filter())
async def weather_callback_handler(
    callback: CallbackQuery, callback_data: WeatherCallback
):

    # load_msg = await WeatherService.get_loading_message()
    # await callback.answer(load_msg)
    # await callback.message.answer(load_msg)

    # current_weather = await WeatherService.get_current_weather()

    if callback_data.action == "weather_menu":

        await callback.message.edit_text(
            text=get_message("RU_LN")["weather_m"]["message"],
            reply_markup=get_inl_btns_weather(),
        )

    if callback_data.action == "weather_get_back":

        main_menu_text = f"""{get_message("RU_LN")["start_m"]["message1"]}{"Пользователь"}{get_message("RU_LN")["start_m"]["message2"]}"""
        _lg.debug(f"{main_menu_text}")

        await callback.message.edit_text(
            text=main_menu_text,
            reply_markup=get_inl_btns_start(),
        )


# обработка команды /weather_menu
@router.message(Command("weather_menu"))
async def command_weather_handler(message: Message):

    await message.answer(
        text=get_message("RU_LN")["weather_m"]["message"],
        reply_markup=get_inl_btns_weather(),
    )
