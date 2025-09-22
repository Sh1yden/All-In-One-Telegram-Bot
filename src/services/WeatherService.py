import os
import json

# Место для импорта всех сервисов
from src.services.OpenMeteo import OpenMeteo
from src.services.GeocodingOMAPI import GeocodingOMAPI
from src.services.VisualCrossing import VisualCrossing
from src.services.WeatherAPI import WeatherAPI
from src.services.YandexAPI import YandexAPI

from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger


class WeatherService:

    def __init__(self):

        self._lg = get_logger()
        self._lg.debug("Logger init.")

        self._appcfg = AppConfig()

    # API
    @staticmethod
    def get_weather_now():
        return

    @staticmethod
    def get_weather_hours():
        return

    @staticmethod
    def get_weather_5d():
        return

    @staticmethod
    def get_weather_day_night():
        return

    @staticmethod
    def get_weather_rain():
        return

    @staticmethod
    def get_weather_wind_pressure():
        return

    @staticmethod
    def get_loading_message():
        return "🔄 Загрузка..."


if __name__ == "__main__":
    ws = WeatherService()
