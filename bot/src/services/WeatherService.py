from typing import Any

from src.services.OpenMeteo import OpenMeteo
from src.core.Logging import get_logger


# TODO переделать всё под бд


class WeatherService:
    """Service for weather data management and API coordination"""

    def __init__(self) -> None:
        self._lg = get_logger()
        self._lg.debug("Logger init.")

        self._open_meteo = OpenMeteo()

    def get_weather_now(self, user_id: int) -> dict[str, Any] | None:
        """
        Get current weather for user

        Args:
            user_id: User ID

        Returns:
            dict | None: Weather data or None if error
        """
        try:
            # TODO переделать
            usr_loc = ""

            if not usr_loc:
                self._lg.warning(f"No location found for user {user_id}")
                return None

            lat = usr_loc.get("latitude")
            lon = usr_loc.get("longitude")

            # Validate coordinates
            if lat is None or lon is None:
                self._lg.warning(f"Missing coordinates for user {user_id}")
                return None

            try:
                lat = float(lat)
                lon = float(lon)
            except (ValueError, TypeError):
                self._lg.warning(f"Invalid coordinates for user {user_id}")
                return None

            # Get weather from OpenMeteo
            user_weather_now_open_meteo = self._open_meteo.get_weather_now_api(lat, lon)

            if not user_weather_now_open_meteo:
                self._lg.error("Failed to get weather from OpenMeteo")
                return None

            user_weather_now_all = {"OpenMeteo": user_weather_now_open_meteo}

            return user_weather_now_all

        except Exception as e:
            self._lg.error(f"Internal error: {e}")
            return None

    @staticmethod
    def get_weather_hours() -> None:
        """Get hourly weather forecast - NOT IMPLEMENTED"""
        pass

    @staticmethod
    async def get_weather_5d() -> None:
        """Get 5-day weather forecast - NOT IMPLEMENTED"""
        pass

    @staticmethod
    async def get_weather_day_night() -> None:
        """Get day/night weather - NOT IMPLEMENTED"""
        pass

    @staticmethod
    async def get_weather_rain() -> None:
        """Get precipitation data - NOT IMPLEMENTED"""
        pass

    @staticmethod
    async def get_weather_wind_pressure() -> None:
        """Get wind and pressure data - NOT IMPLEMENTED"""
        pass

    @staticmethod
    def get_loading_message() -> str:
        """Get loading message text"""
        return "🔄 Загрузка..."


if __name__ == "__main__":
    ws = WeatherService()
    result = ws.get_weather_now(5080080714)
    print(f"Weather data: {result}")
