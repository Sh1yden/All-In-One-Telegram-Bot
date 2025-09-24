import requests
from src.core.Logging import get_logger


class GeocodingOMAPI:

    def __init__(self):

        self._lg = get_logger()
        self._lg.debug("Logger init.")

    def get_location_phone(self, lat: float, lot: float):
        try:
            self._lg.debug("Start get location on PHONE device.")

            req = f"https://open-meteo.com/en/docs?latitude={lat}&longitude={lot}"

            return req

        except Exception as e:
            self._lg.critical(f"Internal error: {e}")

    def get_location_pc(self, name_city: str):
        try:
            self._lg.debug("Start get location on PC device.")

            data = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={name_city}language=ru&format=json"
            )

            lat = data["results"][0]["latitude"]
            lot = data["results"][0]["longitude"]

            req = f"https://open-meteo.com/en/docs?latitude={lat}&longitude={lot}"

            return req

        except Exception as e:
            self._lg.critical(f"Internal error: {e}")


if __name__ == "__main__":
    gc = GeocodingOMAPI()
