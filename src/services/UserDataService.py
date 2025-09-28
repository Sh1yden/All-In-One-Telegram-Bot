import datetime
from pathlib import Path
from typing import Dict, Any

from src.config.AppConfig import AppConfig

from src.core.Logging import get_logger
from src.config.TextMessages import get_message


class UserDataService:
    """Сервис для работы с пользовательскими данными (локация, имя и т.д.)"""

    def __init__(self):
        self._lg = get_logger()
        self._appcfg = AppConfig()

        # Путь к файлу с пользовательскими данными
        self._USR_DATA_FILE = Path(self._appcfg._SAVE_SET_DIR / "users_data.json")

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
            return f"{get_message("RU_LN")["location_m"]["message_good_loc_w_phone"]}{lat}{get_message("RU_LN")["location_m"]["message_good_loc_l_phone"]}{lon}"

        elif location["type"] == "pc":

            lat = location.get("latitude", 0)
            lon = location.get("longitude", 0)
            return f"{get_message("RU_LN")["location_m"]["message_good_loc_w_phone"]}{lat}{get_message("RU_LN")["location_m"]["message_good_loc_l_phone"]}{lon}"

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
        latitude=55.7558,
        longitude=37.6176,
    )

    # Тест получения локации
    location = service.get_user_location(123456)
    print(f"Location: {location}")

    # Тест форматирования
    formatted = service.format_user_location(123456)
    print(f"Formatted: {formatted}")
