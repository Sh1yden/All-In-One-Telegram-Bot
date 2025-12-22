import sys
from pathlib import Path
import re

# Для прямого запуска файла
if __name__ == "__main__":
    # Добавляем bot/ в sys.path
    bot_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(bot_dir))

import asyncio

from fluentogram import TranslatorRunner

from src.core import get_logger
from src.services import get_cord_from_city
from src.utils import (
    Language,
    get_raw_link_api,
    get_soup,
    headers_factory,
    parse_data,
)

_lg = get_logger(__name__)


async def _get_is_day(
    hourly_w: list,
    ERROR: str,
    now_time: int,
    index_list: list = [
        "Восход",
        "Закат",
        "Sunrise",
        "Sunset",
    ],
) -> bool | str | None:
    try:
        _lg.debug(f"Now_time is - {now_time}")

        sun_rise_set = []

        for i in hourly_w:
            # TODO переделать еще и на англ яз
            if re.findall(index_list[0], i) or re.findall(index_list[1], i):
                sun_rise_set.append(i)

        _lg.debug(f"Sun_rise_set is - {sun_rise_set}")

        sunrise_time = int(sun_rise_set[0][:2])
        sunset_time = int(sun_rise_set[1][:2])

        _lg.debug(f"Sunrise_time is - {sunrise_time}")
        _lg.debug(f"Sunset_time is - {sunset_time}")

        if now_time > sunrise_time and now_time < sunset_time:
            is_day = True
        elif now_time > sunrise_time and now_time > sunset_time:
            is_day = False
        else:
            is_day = ERROR

        return is_day
    except Exception as e:
        _lg.error(f"Internal error: {e}")


async def yan_get_weather_now(
    locale: TranslatorRunner | None,
    city: str | None = None,
    latitude: str | float | None = None,
    longitude: str | float | None = None,
):
    """
    Locale = None ONLY for test. \n
    Needed city or lat and lon.
    """  # TODO
    try:
        url = await get_raw_link_api(api_name="YandexParser")

        if url is None:
            return None

        url = url.replace("{lang}", "ru")  # TODO
        _lg.debug(f"Url is - {url}")

        if city is not None and latitude is None and longitude is None:
            cord = await get_cord_from_city(name_city=city)

            latitude = cord.get("lat", None)
            longitude = cord.get("lon", None)

            if latitude is None or longitude is None:
                _lg.warning(
                    f"Latitude: {latitude}, and Longitude: {longitude}. Error request get_cord_from_city."
                )

        params = {
            "lat": latitude,
            "lon": longitude,
        }

        headers = await headers_factory(
            lang=Language.RU,
            is_api=False,
        )
        _lg.debug(f"Headers is - {headers}")

        par_data = await parse_data(
            url=url,
            params=params,
            headers=headers,
        )

        soup = await get_soup(par_data)

        if soup is None:
            _lg.debug("Soup is None!!")
            return None

        if locale is None:
            ERROR = "❌ Ошибка: не удалось получить данные от сервиса."  # ! Для теста
        else:
            ERROR = (
                locale.message_service_error_not_found_in_service()
            )  # ! Для теста без locale, locale=None

        scroll_content = soup.find_all("li", class_="AppHourlyItem_container__aqC1z")
        hourly_w = [i.text for i in scroll_content]
        time = hourly_w[0][:5]
        is_day = await _get_is_day(hourly_w, ERROR, int(time[:2]))
        feels_like = soup.find(
            "span", class_="AppFact_feels__IJoel AppFact_feels_withYesterday__yE440"
        ).text[-3:-1]
        temp = soup.find("p", class_="AppFactTemperature_content__Lx4p9").text[:-1]
        temp_unit = soup.find("p", class_="AppFactTemperature_content__Lx4p9").text[-1:]
        raw_wphc = soup.find_all("li", class_="AppFact_details__item__QFIXI")
        wphc_list = [i.text for i in raw_wphc]
        raw_wind = wphc_list[0].split(",")
        wind = round(float(raw_wind[0][:-3].strip()))
        wind_unit = raw_wind[0][-3:].strip()
        weather_code = soup.find("p", class_="AppFact_warning__8kUUn").text
        humidity = wphc_list[2][:-1]
        humidity_unit = wphc_list[2][-1:]

        _lg.debug(f"Soup is - {bool(soup)}")
        _lg.debug(f"Scroll_content is - {bool(scroll_content)}")
        _lg.debug(f"Hourly_w is - {bool(hourly_w)}.")
        _lg.debug(f"Time is - {time}.")
        _lg.debug(f"Is_day is - {is_day}.")
        _lg.debug(f"Feels_like is - {feels_like}.")
        _lg.debug(f"Temp is - {temp}.")
        _lg.debug(f"Temp_unit is - {temp_unit}.")
        _lg.debug(f"Raw_wphc is - {bool(raw_wphc)}.")
        _lg.debug(f"Wphc_list is - {wphc_list}.")
        _lg.debug(f"Raw_wind is - {raw_wind}.")
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

        YandexParser_data = await yan_get_weather_now(
            locale=None,
            latitude=latitude,
            longitude=longitude,
        )

        all_data: dict = {
            "YandexParser": YandexParser_data,
        }

        _lg.debug(f"All_data is - {bool(all_data)}")

    asyncio.run(main())
