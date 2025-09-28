import requests
from src.core.Logging import get_logger


class GeocodingOMAPI:

    def __init__(self):

        self._lg = get_logger()
        self._lg.debug("Logger init.")

    def get_link_location_phone(self, lat: float, lon: float) -> str | None:
        try:
            self._lg.debug("Start get location on PHONE device.")

            req = f"https://open-meteo.com/en/docs?latitude={lat}&longitude={lon}&language=ru&format=json"

            return req

        except Exception as e:
            self._lg.error(f"Internal error: {e}")

    def get_link_location_pc(self, name_city: str) -> str | None:
        try:
            self._lg.debug("Start get location on PC device.")

            data = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={name_city}&language=ru&format=json"
            ).json()

            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]

            req = f"https://open-meteo.com/en/docs?latitude={lat}&longitude={lon}&language=ru&format=json"

            return req

        except Exception as e:
            self._lg.error(f"Internal error: {e}")

    def get_cord_from_pc(self, name_city: str | None) -> dict | None:
        try:
            self._lg.debug("Start get location on PC device.")

            data = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={name_city}&language=ru&format=json"
            ).json()

            self._lg.debug(f"DATA FROM CORD - {data}")

            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]

            self._lg.debug(f"LAT - {lat}, LON - {lon}")

            cord = {"lat": lat, "lon": lon}

            return cord

        except Exception as e:
            self._lg.error(f"Internal error: {e}")


if __name__ == "__main__":
    gc = GeocodingOMAPI()
