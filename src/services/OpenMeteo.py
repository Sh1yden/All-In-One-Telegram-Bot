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

    def get_weather_now_api(self, lat: float, lon: float):
        try:
            req = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=&current=temperature_2m,is_day,relative_humidity_2m,weather_code,cloud_cover,wind_speed_10m&timezone=auto"
            )

            data = req.json()

            return data

        except Exception as e:
            self._lg.error(f"Internal error: {e}")


if __name__ == "__main__":
    om = OpenMeteo()
