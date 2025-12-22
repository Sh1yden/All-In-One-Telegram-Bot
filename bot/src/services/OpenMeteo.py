import sys
from pathlib import Path

# Для прямого запуска файла
if __name__ == "__main__":
    # Добавляем bot/ в sys.path
    bot_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(bot_dir))

import asyncio

from fluentogram import TranslatorRunner

from src.core import get_logger
from src.services import get_cord_from_city
from src.utils import get_raw_link_api, req_data

_lg = get_logger(__name__)


async def opm_get_weather_now(
    locale: TranslatorRunner | None,
    city: str | None = None,
    latitude: str | float | None = None,
    longitude: str | float | None = None,
) -> dict[str, dict[str, str | bool | None]] | None:
    """
    Locale = None ONLY for test. \n
    Needed city or lat and lon.
    """  # TODO
    try:
        url = await get_raw_link_api(api_name="OpenMeteo")

        if url is None:
            return None

        if city is not None and latitude is None and longitude is None:
            cord = await get_cord_from_city(name_city=city)

            latitude = cord.get("lat", None)
            longitude = cord.get("lon", None)

            if latitude is None or longitude is None:
                _lg.warning(
                    f"Latitude: {latitude}, and Longitude: {longitude}. Error request get_cord_from_city."
                )

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "apparent_temperature",
                "is_day",
                "relative_humidity_2m",
                "weather_code",
                "cloud_cover",
                "wind_speed_10m",
            ],
            "wind_speed_unit": "ms",
            "timezone": "auto",
        }

        req_res = await req_data(url=url, params=params)

        if locale is None:
            ERROR = "❌ Ошибка: не удалось получить данные от сервиса."  # ! Для теста
        else:
            ERROR = (
                locale.message_service_error_not_found_in_service()
            )  # ! Для теста без locale, locale=None

        current_values = req_res.get("current", ERROR)
        current_units = req_res.get("current_units", ERROR)

        raw_time = current_values.get("time", None)
        if raw_time is None:
            time = ERROR
        time = raw_time[11:]
        is_day = bool(current_values.get("is_day", ERROR))
        feels_like = round(current_values.get("apparent_temperature", ERROR))
        temp = round(current_values.get("temperature_2m", ERROR))
        temp_unit = current_units.get("temperature_2m", ERROR)
        wind = round(current_values.get("wind_speed_10m", ERROR))
        wind_unit = current_units.get("wind_speed_10m", ERROR)
        weather_code = current_values.get("weather_code", ERROR)
        humidity = round(current_values.get("relative_humidity_2m", ERROR))
        humidity_unit = current_units.get("relative_humidity_2m", ERROR)

        _lg.debug(f"Req_res is - {req_res}.")
        _lg.debug(f"Raw_time is - {raw_time}.")
        _lg.debug(f"Time is - {time}.")
        _lg.debug(f"Is_day is - {is_day}.")
        _lg.debug(f"Feels_like is - {feels_like}.")
        _lg.debug(f"Temp is - {temp}.")
        _lg.debug(f"Temp_unit is - {temp_unit}.")
        _lg.debug(f"Wind is - {wind}.")
        _lg.debug(f"Wind_unit is - {wind_unit}.")
        _lg.debug(f"Weather_code is - {weather_code}.")
        _lg.debug(f"Humidity is - {humidity}.")
        _lg.debug(f"Humidity_unit is - {humidity_unit}.")

        current_weather_dict = {
            "time": time,
            "is_day": is_day,
            "feels_like": feels_like,
            "temp": temp,
            "temp_unit": temp_unit,
            "wind": wind,
            "wind_unit": wind_unit,
            "weather_code": weather_code,
            "humidity": humidity,
            "humidity_unit": humidity_unit,
        }

        _lg.debug(f"Current_weather_dict is - {current_weather_dict}.")

        return current_weather_dict

    except Exception as e:
        _lg.error(f"Internal error: {e}")


if __name__ == "__main__":

    async def main():
        from src.core import setup_logging

        setup_logging(level="DEBUG")

        latitude = 51.73733
        longitude = 36.18735

        OpenMeteo_data = await opm_get_weather_now(
            locale=None,
            latitude=latitude,
            longitude=longitude,
        )

        all_data: dict = {
            "OpenMeteo": OpenMeteo_data,
        }

        _lg.debug(f"All_data is - {bool(all_data)}")

    asyncio.run(main())
