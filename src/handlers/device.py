from aiogram.types import Message, CallbackQuery, InaccessibleMessage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router

from src.callbacks.DeviceCallback import DeviceCallback
from src.states.LocationState import LocationState

from src.keyboards.k_device import get_inl_btns_device
from src.keyboards.k_location import get_inl_btns_location  # REPLY BTNS
from src.core.Logging import get_logger
from src.config.TextMessages import get_message


router = Router()
_lg = get_logger()


@router.callback_query(DeviceCallback.filter())
async def device_callback_handler(
    callback: CallbackQuery, callback_data: DeviceCallback, state: FSMContext
):

    # Проверяем, что сообщение доступно для редактирования
    if isinstance(callback.message, InaccessibleMessage):
        _lg.warning("Cannot edit inaccessible message.")
        await callback.answer("Сообщение нельзя изменить.")
        return

    message: Message | None = callback.message

    if callback_data.action == "device_phone":

        # Установить состояние ожидания геолокации
        await state.set_state(LocationState.waiting_for_city_phone)

        await message.answer(
            text=get_message("RU_LN")["location_m"]["message_send_loc_phone"],
            reply_markup=get_inl_btns_location(),
        )

    if callback_data.action == "device_pc":

        # Установить состояние ожидания города
        await state.set_state(LocationState.waiting_for_city_pc)

        # Сообщение ожидания названии локации
        await message.answer(
            text=get_message("RU_LN")["location_m"]["message_send_loc_pc"]
        )


@router.message(Command("device"))
async def command_device_handler(message: Message):

    await message.answer(
        text=get_message("RU_LN")["device_m"],
        reply_markup=get_inl_btns_device(),
    )
