import os
import json

from aiogram.fsm.context import FSMContext

# Место для импорта всех сервисов
# from src.services.GeocodingOMAPI import GeocodingOMAPI  # GEO POS
from src.services.OpenMeteo import OpenMeteo  # API
from src.services.VisualCrossing import VisualCrossing  # API
from src.services.WeatherAPI import WeatherAPI  # API
from src.services.YandexAPI import YandexAPI  # API

from src.config.AppConfig import AppConfig
from src.core.Logging import get_logger


class WeatherService:

    def __init__(self):

        self._lg = get_logger()
        self._lg.debug("Logger init.")

        self._appcfg = AppConfig()

    # API
    @staticmethod
    async def get_weather_now() -> str:
        return ""

    @staticmethod
    async def get_weather_hours():
        return

    @staticmethod
    async def get_weather_5d():
        return

    @staticmethod
    async def get_weather_day_night():
        return

    @staticmethod
    async def get_weather_rain():
        return

    @staticmethod
    async def get_weather_wind_pressure():
        return

    @staticmethod
    async def get_loading_message():
        return "🔄 Загрузка..."


if __name__ == "__main__":
    ws = WeatherService()
