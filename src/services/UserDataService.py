import datetime
from pathlib import Path
from typing import Dict, Any

from src.config.AppConfig import AppConfig

# from src.services.GeocodingOMAPI import get_cord_from_city
from src.services.NominatimAPI import get_city_from_cord

from src.core.Logging import get_logger
from src.config.TextMessages import get_message


class UserDataService:
    """Сервис для работы с пользовательскими данными (локация, имя и т.д.)"""

    def __init__(self):

        self._lg = get_logger()
        self._appcfg = AppConfig()

        # Путь к файлу с пользовательскими данными
        self._USR_DATA_FILE = Path(self._appcfg.get_save_set_dir, "users_data.json")

    def save_user_location(
        self,
        user_id: int,
        username: str,
        full_name: str,
        location_type: str,
        **location_data,
    ) -> bool:
        """
        Сохранить локацию пользователя в файл

        Args:
            user_id: ID пользователя в телеграм
            username: Username пользователя
            full_name: Полное имя пользователя
            location_type: Тип локации ("phone" или "pc")
            **location_data: Дополнительные данные (latitude, longitude, city)

        Returns:
            bool: Успешность сохранения
        """
        try:
            data = self._appcfg.load_from_file(self._USR_DATA_FILE)

            if not data:
                data = {"users": {}}

            user_key = str(user_id)
            current_time = datetime.datetime.now().isoformat()

            # Подготовить данные пользователя
            user_info = {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "location": {
                    "type": location_type,
                    "updated_at": current_time,
                    **location_data,
                },
                "last_activity": current_time,
            }

            # Если пользователь уже есть, обновить только локацию и активность
            if user_key in data["users"]:
                data["users"][user_key].update(
                    {
                        "username": username,
                        "full_name": full_name,
                        "location": user_info["location"],
                        "last_activity": current_time,
                    }
                )
            else:
                data["users"][user_key] = user_info

            # Сохранить в файл
            self._appcfg.save_to_file(self._USR_DATA_FILE, data)

            self._lg.info(
                f"Saved location for user {user_id} ({full_name}): {location_type}"
            )
            return True

        except Exception as e:
            self._lg.error(f"Error saving user location: {e}")
            return False

    def _has_null_location(self, user_id: int) -> bool:
        """Проверить есть ли NULL значения в локации пользователя"""
        location = user_data_service.get_user_location(user_id)

        if not location:
            return False

        # Проверяем каждое поле на NULL
        if (
            location.get("city") is None
            or location.get("latitude") is None
            or location.get("longitude") is None
        ):
            return True

        return False

    def _fix_null_location(self, user_id: int) -> bool:
        """
        Исправить NULL значения в локации пользователя
        Пытается получить данные через API на основе имеющихся координат
        """
        try:
            location = user_data_service.get_user_location(user_id)

            if not location:
                self._lg.warning(f"No location found for user {user_id}")
                return False

            changes_made = False
            lat = location.get("latitude")
            lon = location.get("longitude")
            city = location.get("city")

            # Если есть координаты но нет города - получаем через reverse geocoding
            if lat is not None and lon is not None and (city is None or city == ""):
                try:
                    city = get_city_from_cord(lat, lon, user_agent="TestApp/1.0")
                    if city:
                        self._lg.info(f"Fixed NULL city for user {user_id}: {city}")
                        changes_made = True
                except Exception as e:
                    self._lg.warning(f"Failed to get city from coordinates: {e}")

            # Если были изменения - перезаписываем локацию
            if changes_made:
                user_data = user_data_service.get_user_info(user_id)
                if user_data:
                    success = user_data_service.save_user_location(
                        user_id=user_id,
                        username=user_data.get("username", ""),
                        full_name=user_data.get("full_name", "Unknown"),
                        location_type=location.get("type", "phone"),
                        city=city,
                        latitude=lat,
                        longitude=lon,
                    )
                    return success

            return changes_made

        except Exception as e:
            self._lg.error(f"Error fixing NULL location: {e}")
            return False

    def get_user_location(self, user_id: int) -> Dict[str, Any] | None:
        """
        Получить сохраненную локацию пользователя

        Args:
            user_id: ID пользователя

        Returns:
            dict | None: Данные локации или None если не найдено
        """
        try:
            data = self._appcfg.load_from_file(self._USR_DATA_FILE)

            if not data or "users" not in data:
                return None

            user_key = str(user_id)
            user_data = data["users"].get(user_key)

            if not user_data or "location" not in user_data:
                return None

            self._lg.debug(f"Retrieved location for user {user_id}")
            return user_data["location"]

        except Exception as e:
            self._lg.error(f"Error getting user location: {e}")
            return None

    def get_usr_one_loc_par(self, user_id: int, loc_key: str) -> str:
        try:
            par = user_data_service.get_user_location(user_id) or {}
            # Если город не указан
            par_text = get_message("RU_LN")["location_m"]["message_loc_not_post"]

            # Проверка на то указан ли город
            if par and isinstance(par, dict) and par.get(loc_key):
                par_text = par[loc_key]

            return par_text

        except Exception as e:
            self._lg.error(f"Error getting user info: {e}")
            return get_message("RU_LN")["location_m"]["message_loc_not_post"]

    def get_user_info(self, user_id: int) -> Dict[str, Any] | None:
        """
        Получить полную информацию о пользователе

        Args:
            user_id: ID пользователя

        Returns:
            dict | None: Данные пользователя или None если не найдено
        """
        try:
            data = self._appcfg.load_from_file(self._USR_DATA_FILE)

            if not data or "users" not in data:
                return None

            user_key = str(user_id)
            return data["users"].get(user_key)

        except Exception as e:
            self._lg.error(f"Error getting user info: {e}")
            return None

    def user_has_location(self, user_id: int) -> bool:
        """
        Проверить, есть ли у пользователя сохраненная локация

        Args:
            user_id: ID пользователя

        Returns:
            bool: True если локация есть
        """
        location = self.get_user_location(user_id)
        return location is not None

    def format_user_location(self, user_id: int) -> str:
        """
        Отформатировать локацию пользователя для отображения

        Args:
            user_id: ID пользователя

        Returns:
            str: Отформатированная строка с локацией
        """
        location = self.get_user_location(user_id)

        if not location:
            return get_message("RU_LN")["location_m"]["message_loc_not_post"]

        if location["type"] == "phone":

            lat = location.get("latitude", 0)
            lon = location.get("longitude", 0)
            city = location.get("city")

            return f"{get_message("RU_LN")["location_m"]["message_good_loc_city_pc"]}{city}\n{get_message("RU_LN")["location_m"]["message_good_loc_w_phone"]}{lat}{get_message("RU_LN")["location_m"]["message_good_loc_l_phone"]}{lon}"

        elif location["type"] == "pc":

            lat = location.get("latitude", 0)
            lon = location.get("longitude", 0)
            city = location.get("city")

            return f"{get_message("RU_LN")["location_m"]["message_good_loc_city_pc"]}{city}\n{get_message("RU_LN")["location_m"]["message_good_loc_w_phone"]}{lat}{get_message("RU_LN")["location_m"]["message_good_loc_l_phone"]}{lon}"

        else:
            return get_message("RU_LN")["location_m"]["message_unknown_loc"]

    def delete_user_data(self, user_id: int) -> bool:
        """
        Удалить все данные пользователя

        Args:
            user_id: ID пользователя

        Returns:
            bool: Успешность удаления
        """
        try:
            data = self._appcfg.load_from_file(self._USR_DATA_FILE)

            if not data or "users" not in data:
                return False

            user_key = str(user_id)

            if user_key in data["users"]:
                del data["users"][user_key]
                self._appcfg.save_to_file(self._USR_DATA_FILE, data)
                self._lg.info(f"Deleted data for user {user_id}")
                return True

            return False

        except Exception as e:
            self._lg.error(f"Error deleting user data: {e}")
            return False


# Глобальный экземпляр сервиса
user_data_service = UserDataService()


if __name__ == "__main__":
    # Тестирование
    service = UserDataService()

    # Тест сохранения локации с телефона
    service.save_user_location(
        user_id=123456,
        username="test_user",
        full_name="Test User",
        location_type="phone",
        city="Курск",
        latitude=55.7558,
        longitude=37.6176,
    )

    info = service.get_user_info(123456)
    if info is None:
        service._lg.debug(f"INFO IS NONE!!!!")
    else:
        ifo = info.get("location")
        service._lg.debug(f"USER info: {ifo}")

    # Тест получения локации
    location = service.get_user_location(123456)
    service._lg.debug(f"Location: {location}")

    # Тест получения одного параметра локации
    one_par = service.get_usr_one_loc_par(123456, "c")
    service._lg.debug(f"One par: {one_par}")

    # Тест форматирования
    formatted = service.format_user_location(123456)
    service._lg.debug(f"Formatted: {formatted}")
