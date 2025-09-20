import os
from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger

_appcfg = AppConfig()
_lg = get_logger()
_lg.debug("Logger init.")


def get_token():

    try:
        _lg.debug("Getting token.")

        _TOKEN_PATH = os.path.expanduser(
            "~\\Documents\\All Code Programming\\_secret_api_keys\\api_keys.json"
        )

        data = _appcfg.load_from_file(_TOKEN_PATH)

        if not data:
            _lg.debug("Token file is empty or failed to load.")
            return None

        token = data.get("AIO_BOT_TOKEN")  # Исправление KeyError
        if token:
            _lg.debug("Token loaded successfully.")
            return token
        else:
            _lg.warning("Token key 'AIO_BOT_TOKEN' not found in file.")
            return None

    except Exception as e:
        _lg.critical(f"Internal error: {e}.")


if __name__ == "__main__":
    print(True if get_token() else False)
