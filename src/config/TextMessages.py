from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger

_appcfg = AppConfig()
_lg = get_logger()
_lg.debug("Logger init.")


def get_message(key: str | None = None) -> dict | None:
    """Универсальный метод. Не вводите ключ, если хотите получить весь файл с сообщениями."""
    try:
        _lg.debug(f"Loading messages, key={key}")
        data = _appcfg.load_from_file(_appcfg.save_set_msg_file)

        if not isinstance(data, dict):
            _lg.warning("Loaded data is not a dictionary.")
            return None

        if key is None:
            _lg.debug("Returning all messages.")
            return data or None

        # Получаем по ключу
        result = data.get(key)
        if result is None:
            _lg.warning(f"Key '{key}' not found in messages.")
        else:
            _lg.debug(f"Key '{key}' loaded successfully.")

        return result

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


if __name__ == "__main__":
    _lg.debug(get_message("RU_LN")["start_m"])
