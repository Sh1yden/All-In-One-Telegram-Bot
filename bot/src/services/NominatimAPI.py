import requests
from typing import Any

from src.core.Logging import get_logger


_lg = get_logger()


def get_city_from_cord(
    latitude: float, longitude: float, user_agent: str = "MyApp/1.0"
) -> str | None:
    """
    Get city name from coordinates using Nominatim reverse geocoding.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        user_agent: User-Agent header value

    Returns:
        str | None: City name or None if request failed
    """
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "zoom": 10,
        "addressdetails": 1,
    }
    headers = {"User-Agent": user_agent}

    try:
        _lg.debug(f"Requesting city name for coordinates: {latitude}, {longitude}")

        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()

    except requests.Timeout:
        _lg.error("Nominatim API request timeout")
        return None
    except requests.RequestException as e:
        _lg.error(f"Request error: {e}")
        return None

    try:
        data = response.json()

        if not isinstance(data, dict):
            _lg.warning("Invalid response structure from Nominatim API")
            return None

        address = data.get("address")

        if not isinstance(address, dict):
            _lg.warning("Missing or invalid 'address' in API response")
            return None

        # Try to get city name in order of priority
        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or address.get("county")
        )

        if city:
            _lg.debug(f"City found: {city}")
        else:
            _lg.warning(f"No city found for coordinates: {latitude}, {longitude}")

        return city

    except ValueError as e:
        _lg.error(f"Error parsing JSON response: {e}")
        return None
    except (KeyError, AttributeError) as e:
        _lg.error(f"Error accessing response data: {e}")
        return None
    except Exception as e:
        _lg.error(f"Unexpected error: {e}")
        return None


if __name__ == "__main__":
    lat, lon = 51.705684, 36.164215  # Kursk coordinates
    city = get_city_from_cord(lat, lon, user_agent="TestApp/1.0")
    print(f"City: {city}")
