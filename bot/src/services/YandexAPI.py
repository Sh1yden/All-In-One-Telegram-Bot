import os
from src.core import get_logger


# Тут будет вместо использования API, парсинг
# TODO сделать парсинг данных YANDEX


class YandexAPI:

    def __init__(self):

        self._lg = get_logger()
        self._lg.debug("Logger init.")

        # ! YANDEX платно, плохая дока потом
