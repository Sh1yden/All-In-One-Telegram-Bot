import requests
from typing import Optional


def get_city_from_cord(
    latitude: float, longitude: float, user_agent: str = "MyApp/1.0"
) -> Optional[str]:
    """
    Get city name from coordinates using Nominatim.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        user_agent: User-Agent header value

    Returns:
        City name or None if request failed
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
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

    try:
        data = response.json()
        address = data.get("address", {})

        # Try to get city name in order of priority
        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or address.get("county")
        )

        return city
    except (ValueError, KeyError) as e:
        print(f"Parse error: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    lat, lon = 51.705684, 36.164215  # Kursk coordinates
    city = get_city_from_cord(lat, lon, user_agent="TestApp/1.0")
    print(f"City: {city}")
