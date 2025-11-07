import requests
from typing import Any

from src.core.Logging import get_logger


_lg = get_logger()


def get_link_location_phone(lat: float, lon: float) -> str | None:
    """
    Generate link for phone location

    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate

    Returns:
        str | None: Link to location or None if error
    """
    try:
        _lg.debug("Start get location on PHONE device.")

        req = (
            f"https://open-meteo.com/en/docs?latitude={lat}&longitude={lon}"
            f"&language=ru&format=json"
        )

        return req

    except Exception as e:
        _lg.error(f"Internal error: {e}")
        return None


def get_link_location_pc(name_city: str) -> str | None:
    """
    Generate link for PC location by city name

    Args:
        name_city: City name

    Returns:
        str | None: Link to location or None if error
    """
    try:
        _lg.debug("Start get location on PC device.")

        response = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?"
            f"name={name_city}&language=ru&format=json",
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()

        # Validate API response
        if (
            not isinstance(data, dict)
            or "results" not in data
            or not isinstance(data["results"], list)
            or len(data["results"]) == 0
        ):
            _lg.warning(f"No results found for city: {name_city}")
            return None

        result = data["results"][0]
        lat = result.get("latitude")
        lon = result.get("longitude")

        if lat is None or lon is None:
            _lg.warning(f"Missing coordinates in API response for city: {name_city}")
            return None

        req = (
            f"https://open-meteo.com/en/docs?latitude={lat}&longitude={lon}"
            f"&language=ru&format=json"
        )

        return req

    except requests.RequestException as e:
        _lg.error(f"Request error: {e}")
        return None
    except (KeyError, IndexError, TypeError) as e:
        _lg.error(f"Error parsing API response: {e}")
        return None
    except Exception as e:
        _lg.error(f"Internal error: {e}")
        return None


def get_cord_from_city(name_city: str | None) -> dict[str, float] | None:
    """
    Get coordinates from city name using Open-Meteo API

    Args:
        name_city: City name to search

    Returns:
        dict | None: Dictionary with 'lat' and 'lon' keys or None if error
    """
    try:
        if not name_city:
            _lg.warning("City name is empty or None")
            return None

        _lg.debug(f"Getting coordinates for city: {name_city}")

        response = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?"
            f"name={name_city}&language=ru&format=json",
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()

        # Validate API response structure
        if (
            not isinstance(data, dict)
            or "results" not in data
            or not isinstance(data["results"], list)
        ):
            _lg.warning(f"Invalid API response structure for city: {name_city}")
            return None

        if len(data["results"]) == 0:
            _lg.warning(f"No results found for city: {name_city}")
            return None

        result = data["results"][0]
        lat = result.get("latitude")
        lon = result.get("longitude")

        # Validate coordinates exist
        if lat is None or lon is None:
            _lg.warning(f"Missing coordinates in API response for city: {name_city}")
            return None

        # Validate coordinates are valid numbers
        try:
            lat = float(lat)
            lon = float(lon)
        except (ValueError, TypeError):
            _lg.warning(f"Invalid coordinate values for city: {name_city}")
            return None

        cord = {"lat": lat, "lon": lon}

        _lg.debug(f"Retrieved coordinates for {name_city}: {cord}")
        return cord

    except requests.RequestException as e:
        _lg.error(f"Request error: {e}")
        return None
    except (KeyError, IndexError, TypeError) as e:
        _lg.error(f"Error parsing API response: {e}")
        return None
    except Exception as e:
        _lg.error(f"Internal error: {e}")
        return None


if __name__ == "__main__":
    # Test with valid city
    result = get_cord_from_city("Москва")
    print(f"Result: {result}")

    # Test with invalid city
    result = get_cord_from_city("InvalidCityXYZ123")
    print(f"Result: {result}")
