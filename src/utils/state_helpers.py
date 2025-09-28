from aiogram.fsm.context import FSMContext
from src.core.Logging import get_logger

_lg = get_logger()


async def clear_state(state: FSMContext) -> None:
    """
    Очистка состояния FSM

    Args:
        state: FSM контекст
    """
    try:
        await state.clear()
        _lg.debug("State cleared")
    except Exception as e:
        _lg.error(f"Error clearing state: {e}")


async def is_waiting_for_location(state: FSMContext) -> bool:
    """
    Проверить, ожидает ли бот ввод локации

    Args:
        state: FSM контекст

    Returns:
        bool: True если ожидает локацию
    """
    try:
        current_state = await state.get_state()
        return current_state in [
            "LocationState:waiting_for_location_phone",
            "LocationState:waiting_for_city_pc",
        ]
    except Exception as e:
        _lg.error(f"Error checking state: {e}")
        return False
