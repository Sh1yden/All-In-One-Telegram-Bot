from aiogram.types import Message, CallbackQuery, InaccessibleMessage
from aiogram.filters import Command
from aiogram import Router

from src.callbacks.DeviceCallback import DeviceCallback

from src.keyboards.k_device import get_inl_btns_device
from src.keyboards.k_location import get_inl_btns_location  # REPLY BTNS # TODO
from src.core.Logging import get_logger
from src.config.TextMessages import get_message


router = Router()
_lg = get_logger()


@router.callback_query(DeviceCallback.filter())
async def device_callback_handler(
    callback: CallbackQuery, callback_data: DeviceCallback
):

    # Проверяем, что сообщение доступно для редактирования
    if isinstance(callback.message, InaccessibleMessage):
        _lg.warning("Cannot edit inaccessible message.")
        await callback.answer("Сообщение нельзя изменить.")
        return

    message: Message | None = callback.message

    if callback_data.action == "device_phone":

        await message.answer(
            text=get_message("RU_LN")["location_m"]["message1"],
            reply_markup=get_inl_btns_location(),
        )

    if callback_data.action == "device_pc":

        # TODO сделать ручное определение на пк

        # ! Заглушка
        await message.answer(
            text=get_message("RU_LN")["location_m"]["message1"],
            reply_markup=get_inl_btns_location(),
        )


@router.message(Command("device"))
async def command_device_handler(message: Message):

    await message.answer(
        text=get_message("RU_LN")["device_m"],
        reply_markup=get_inl_btns_device(),
    )
