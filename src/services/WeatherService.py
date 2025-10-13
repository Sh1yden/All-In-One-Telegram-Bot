import os
import json

from aiogram.fsm.context import FSMContext

# Место для импорта всех сервисов
from src.services.UserDataService import UserDataService  # SERVICE
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
        self._user_ds = UserDataService()
        self._open_meteo = OpenMeteo()

    # API
    def get_weather_now(self, user_id: int) -> dict | None:
        try:
            usr_loc = self._user_ds.get_user_location(user_id) or {}
            lat = usr_loc.get("latitude", 0)
            lon = usr_loc.get("longitude", 0)

            # OpenMeteo
            user_weather_now_open_meteo = self._open_meteo.get_weather_now_api(lat, lon)
            # VisualCrossing

            # WeatherAPI

            # YandexAPI

            # ALL
            user_weather_now_all = {"OpenMeteo": user_weather_now_open_meteo}

            return user_weather_now_all

        except Exception as e:
            self._lg.error(f"Internal error: {e}")

    @staticmethod
    def get_weather_hours():
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

    ws.get_weather_now(5080080714)
