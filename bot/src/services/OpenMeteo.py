import requests
from typing import Any

from src.core.Logging import get_logger


class OpenMeteo:
    """Service for interacting with Open-Meteo weather API"""

    def __init__(self) -> None:
        self._lg = get_logger()
        self._lg.debug("OpenMeteo service initialized.")

    def get_weather_now_api(self, lat: float, lon: float) -> dict[str, Any] | None:
        """
        Get current weather data from Open-Meteo API

        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate

        Returns:
            dict | None: Weather data or None if error
        """
        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&hourly="
                f"&current=temperature_2m,is_day,relative_humidity_2m,"
                f"weather_code,cloud_cover,wind_speed_10m&timezone=auto"
            )

            self._lg.debug(f"Requesting weather data for {lat}, {lon}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Validate response structure
            if not isinstance(data, dict):
                self._lg.warning("Invalid response structure from API")
                return None

            if "current" not in data:
                self._lg.warning("Missing 'current' key in API response")
                return None

            self._lg.debug("Weather data retrieved successfully")
            return data

        except requests.Timeout:
            self._lg.error("API request timeout")
            return None
        except requests.RequestException as e:
            self._lg.error(f"Request error: {e}")
            return None
        except ValueError as e:
            self._lg.error(f"Error parsing JSON response: {e}")
            return None
        except Exception as e:
            self._lg.error(f"Internal error: {e}")
            return None


if __name__ == "__main__":
    om = OpenMeteo()
    result = om.get_weather_now_api(51.5074, -0.1278)  # London coordinates
    print(f"Weather data: {result}")
