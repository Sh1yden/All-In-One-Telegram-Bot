from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router

from bot.callbacks.WeatherCallback import WeatherCallback  # CALLBACK

# from services.WeatherService import WeatherService  # API

from bot.keyboards.k_weather import get_inl_btns_weather  # BTN
from bot.handlers.start import command_start_handler


router = Router()

_menu_text = "Это меню погоды. Выбрать нужные функции можно под сообщением или написав нужные команды."


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
            text=_menu_text, reply_markup=get_inl_btns_weather()
        )

    if callback_data.action == "weather_get_back":
        await command_start_handler(callback.message)


# обработка команды /weather_menu
@router.message(Command("weather_menu"))
async def command_weather_handler(message: Message):

    await message.answer(text=_menu_text, reply_markup=get_inl_btns_weather())
