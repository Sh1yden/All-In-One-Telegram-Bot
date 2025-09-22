import os
import json
import requests

from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger


class OpenMeteo:

    def __init__(self):

        self._lg = get_logger()
        self._lg.debug("Logger init.")

        self._appcfg = AppConfig()


if __name__ == "__main__":
    om = OpenMeteo()
