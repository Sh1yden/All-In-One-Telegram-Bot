import os

from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger


class YandexAPI:

    def __init__(self):

        self._lg = get_logger()
        self._lg.debug("Logger init.")

        self._appcfg = AppConfig()

        # ! YANDEX платно, плохая дока потом
        self.__YANDEX_ACCESS_PATH = os.path.expanduser(
            "~\\Documents\\All Code Programming\\_secret_api_keys\\api_keys.json"
        )

        self.__YANDEX_ACCESS_KEY = self._appcfg.load_from_file(
            self.__YANDEX_ACCESS_PATH
        )
