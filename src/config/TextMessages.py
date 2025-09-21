from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger

_appcfg = AppConfig()
_lg = get_logger()
_lg.debug("Logger init.")


def get_message(key: str | None = None) -> dict:
    """
    Универсальный метод для получения сообщений.
    - Если key=None — возвращает весь словарь сообщений (или {} если не удалось загрузить).
    - Если key передан — возвращает подсловарь по ключу (или {} если ключ не найден).
    - Никогда не возвращает None — всегда dict.
    """
    try:
        _lg.debug(f"Loading messages, key={key}")
        data = _appcfg.load_from_file(_appcfg.save_set_msg_file)

        if not isinstance(data, dict):
            _lg.warning("Loaded data is not a dictionary. Returning empty dict.")
            return {}

        if key is None:
            _lg.debug("Returning all messages.")
            return data

        # Получаем по ключу
        result = data.get(key)
        _lg.debug(f"RESULT - {type(result)}")

        if result is None:
            _lg.warning(f"Key '{key}' not found in messages. Returning empty dict.")
            return {}
        else:
            _lg.debug(f"Key '{key}' loaded successfully.")
            if not isinstance(result, dict):
                _lg.warning(
                    f"Value for key '{key}' is not a dict. Returning empty dict."
                )
                return {}
            return result

    except Exception as e:
        _lg.critical(f"Internal error:{e}.")
        return {}


if __name__ == "__main__":
    _lg.debug(get_message("RU_LN")["start_m"])
