# ===== APPLICATION CONFIGURATION CLASS / КЛАСС КОНФИГУРАЦИИ ПРИЛОЖЕНИЯ =====
# Application configuration and file management class
# Класс конфигурации приложения и управления файлами

# ===== IMPORTS / ИМПОРТЫ =====
import json
import os
from pathlib import Path
from typing import Any

from src.core.Logging import get_logger


# ===== CONFIGURATION CLASS / КЛАСС КОНФИГУРАЦИИ =====
class AppConfig:
    """
    Application configuration and file management / Настройка и создание конфига для всей программы. Работа с файлами программы.
    Singleton pattern implementation for global settings / Реализация паттерна Singleton для глобальных настроек

    This class manages application configuration files, directories and settings.
    It implements the Singleton pattern to ensure only one instance exists.

    Этот класс управляет конфигурационными файлами приложения, директориями и настройками.
    Он реализует паттерн Singleton для обеспечения существования только одного экземпляра.
    """

    # ===== SINGLETON PATTERN IMPLEMENTATION / РЕАЛИЗАЦИЯ ПАТТЕРНА СИНГЛТОН =====
    _instanse_AppCfg = None  # Stores single instance / Хранит единственный экземпляр
    _initialized_AppCfg = (
        False  # Single initialization flag / Флаг на единственную инициализацию
    )

    # ===== SINGLETON CREATION METHOD / МЕТОД СОЗДАНИЯ СИНГЛТОНА =====
    def __new__(cls):
        """
        Create single class instance / Создание единого объекта класса

        Ensures only one instance of AppConfig exists throughout the application lifecycle.
        Обеспечивает существование только одного экземпляра AppConfig в течение жизни приложения.

        Returns:
            AppConfig: Single instance of the configuration class
        """
        if cls._instanse_AppCfg is None:
            # If no class instance exists, create one / Если экземпляра класса нет создаём
            cls._instanse_AppCfg = super().__new__(cls)
        return cls._instanse_AppCfg

    # ===== INITIALIZATION METHOD / МЕТОД ИНИЦИАЛИЗАЦИИ =====
    def __init__(self):
        """
        Initialize configuration only once / Инициализация конфигурации только один раз

        Initializes all configuration parameters, file paths, and creates necessary directories.
        Sets up logging and database configuration with default values.

        Инициализирует все параметры конфигурации, пути к файлам и создает необходимые директории.
        Настраивает логирование и конфигурацию базы данных со значениями по умолчанию.
        """
        if not AppConfig._initialized_AppCfg:
            # Successful constructor and class initialization / Успешная инициализация конструктора и класса
            AppConfig._initialized_AppCfg = True

            # ===== ERROR HANDLING SETUP / НАСТРОЙКА ОБРАБОТКИ ОШИБОК =====
            # Protection from recursion and other internal errors / Защита от рекурсии и прочих внутренних ошибок
            # Activated automatically when errors occur / Которая включается сама при возникновении ошибок
            # Internal error flag to prevent infinite recursion during error handling
            # Флаг внутренней ошибки для предотвращения бесконечной рекурсии при обработке ошибок
            self._internal_error_occurred = False

            # ===== FILESYSTEM CONFIGURATION / НАСТРОЙКА ФАЙЛОВОЙ СИСТЕМЫ =====
            # Common directories setup / Настройка общих папок
            self._CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
            self._PROJECT_DIR = os.path.dirname(os.path.dirname(self._CURRENT_DIR))
            # Program settings directory / Папка настроек программы
            self._SAVE_SET_DIR = Path(f"{self._PROJECT_DIR}/src/config/settings/")

            # ===== LOGGING CONFIGURATION SETUP / НАСТРОЙКА КОНФИГУРАЦИИ ЛОГИРОВАНИЯ =====
            # Log directory path / Путь к папке для логов
            self._SAVE_LG_DIR = Path(os.path.join(self._PROJECT_DIR, "logs"))

            # Место для db

            # Место для файла текста сообщений
            # TODO EN_LN
            self._SAVE_SET_MSG_FILE = Path(
                os.path.join(self._SAVE_SET_DIR, "text_messages.json")
            )
            # TODO Добавлять новые сообщения
            self._MSG_DEF_FILE = {
                "RU_LN": {
                    "before_start_m": {
                        "message": "Привет🗿👋!  Это бот🤖 All In One(Всё В Одном)📚. \n💼 Тут будет тест различных функций Aiogram и не только. \n ⛅️ Первая будет погода дальше что-нибудь еще(потом дополню это описание). \n 🚀 ЗАПУСТИТЬ: /start."
                    },
                    "start_m": {
                        "message_hello": "Привет🗿👋 ",
                        "message_main_menu": "!\n💼 Тут будет меню выбора различных функций бота.\n🚑 Так же чтобы вывести все команды бота напиши /help.\n⛅️ Вызвать функцию погоды можно нажав кнопку ниже, либо же введя команду /weather_menu.",
                        "buttons": ["⛅️ Погода"],
                    },
                    "help_m": {
                        "message": "🚑 Это хелп меню.📚 Тут будут все команды бота:\n🚀 Начальное меню /start.\n🚑 Вызвать это меню /help.\n⛅️ Меню погоды /weather_menu."
                    },
                    "weather_m": {
                        "message": "⛅️ Это меню погоды. Выбрать нужные функции💼 можно под сообщением или написав нужные команды📚.",
                        "buttons": [
                            "🌡 Сейчас",
                            "📊 Почасовой",
                            "📆 На 5 дней",
                            "🌅 Утро / 🌇 Вечер",
                            "🌦 Осадки",
                            "🧭 Ветер/давление",
                            "⚙️ Настроить",
                            "🔔 Подписка",
                            "📍 Локация: ",
                            "⏪ Назад",
                        ],
                    },
                    "device_m": {
                        "message": "❓ Выберете свой девайс для определения местоположения.",
                        "buttons": ["📱 Телефон", "🖥️💻 Компьютер"],
                    },
                    "location_m": {
                        "message_send_loc_phone": "❗ Пожалуйста, отправьте ваше местоположение:",
                        "message_send_loc_pc": "❗ Пожалуйста, введите текстом ваше местоположение(Город):",
                        "message_good_loc_w_phone": "📍 Получено местоположение:\nШирота: ",
                        "message_good_loc_l_phone": "\nДолгота: ",
                        "message_good_loc_city_pc": "📍 Получено местоположение:\nГород - ",
                        "message_error": "❌ Ошибка сохранения локации",
                        "message_cancel": "❌ Запрос локации отменен.",
                        "buttons": ["📍 Отправить местоположение", "❌ Отмена"],
                    },
                },
                "EN_LN": {},
            }

            # ===== НАСТРОЙКА КОНФИГУРАЦИИ ДЛЯ ПОЛЬЗОВАТЕЛЬСКИХ ДАННЫХ =====
            # Для теста сохранять будем в файл, потом уже для норм в бд # TODO сделать бд
            self._SAVE_SET_USR_FILE = Path(
                os.path.join(self._SAVE_SET_DIR, "users_data.json")
            )
            self._USR_DATA_DEF_FILE = {"users": {}}

            # ===== FILE AND DIRECTORY INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ФАЙЛОВ И ДИРЕКТОРИЙ =====
            self._init_files()

            # Init logger
            self._lg = get_logger()
            self._lg.debug("Logger init.")

    # ===== PROPERTY METHODS - LOGGING CONFIGURATION / МЕТОДЫ-СВОЙСТВА - КОНФИГУРАЦИЯ ЛОГИРОВАНИЯ =====

    @property
    def save_set_msg_file(self) -> Path:
        return self._SAVE_SET_MSG_FILE

    @property
    def save_lg_dir(self) -> Path:
        """
        Get log directory path / Получить путь к папке логов

        Returns:
            Path: Path to the logs directory
        """
        return self._SAVE_LG_DIR

    # ===== PRIVATE METHODS - FILE OPERATIONS / ПРИВАТНЫЕ МЕТОДЫ - ОПЕРАЦИИ С ФАЙЛАМИ =====

    def _init_files(self) -> None:
        """
        Initialize directories and files for the program / Инициализация папок и файлов для программы. Настройки, папка для логов и т.д.

        Creates necessary directories and configuration files if they don't exist.
        Sets up the basic file structure required for the application to function properly.

        Создает необходимые директории и конфигурационные файлы, если они не существуют.
        Настраивает базовую файловую структуру, необходимую для правильной работы приложения.
        """
        try:
            # ===== GENERAL DIRECTORY SETUP / ОБЩАЯ НАСТРОЙКА ДИРЕКТОРИЙ =====
            # Create settings directory if it doesn't exist / Создание папки настроек, если она не существует
            self._SAVE_SET_DIR.mkdir(parents=True, exist_ok=True)

            # ===== LOGGING SETUP / НАСТРОЙКА ЛОГИРОВАНИЯ =====
            # Create log directory if it doesn't exist / Создание папки для логов, если она не существует
            self._SAVE_LG_DIR.mkdir(parents=True, exist_ok=True)

            # Место под bd
            # Пока файл
            if not self._SAVE_SET_USR_FILE.exists():
                self.save_to_file(self._SAVE_SET_USR_FILE, self._USR_DATA_DEF_FILE)

            # Файл текста сообщений
            if not self._SAVE_SET_MSG_FILE.exists():
                self.save_to_file(self._SAVE_SET_MSG_FILE, self._MSG_DEF_FILE)

        except Exception as e:
            # Set internal error flag to prevent infinite recursion / Установка флага внутренней ошибки для предотвращения бесконечной рекурсии
            self._internal_error_occurred = True
            self._lg.critical(f"Internal error: {e}.")

    # ===== PUBLIC METHODS - FILE OPERATIONS / ПУБЛИЧНЫЕ МЕТОДЫ - ОПЕРАЦИИ С ФАЙЛАМИ =====

    def load_from_file(self, file_path: Path | str, mode="r") -> Any | None:
        """
        Load data from JSON file and return its contents / Загрузка данных из JSON файла и возврат его содержания

        Args:
            file_path (Path): Path to the file to load from

        Returns:
            dict: Loaded data from the file, or None if error occurs
        """
        try:
            with open(file_path, mode, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            # Set error flag and return None on failure / Установка флага ошибки и возврат None при неудаче
            self._internal_error_occurred = True
            self._lg.critical(f"Internal error: {e}.")

    def save_to_file(
        self, file_path: Path | str, var: dict, jsonl: bool = False, mode: str = "w"
    ) -> Any | None:
        """
        Save value to JSON file / Сохранение значения в JSON файл
        And Save value to JSONL file / Сохранение значения в JSONL файл

        Args:
            file_path (Path): Path to the file to save to
            var (dict): Data to save to the file
            mode (str): File open mode (used only for JSON). Defaults to "w".
                    Режим открытия файла (используется только для JSON).
            jsonl (bool): If True, save in JSONL format (one object per line).
                          Если True, сохраняет в формате JSONL (по объекту на строку).
        """
        try:
            if jsonl:
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(var, ensure_ascii=False) + "\n")
            else:
                with open(file_path, mode, encoding="utf-8") as f:
                    json.dump(var, f, indent=2, ensure_ascii=False)
        except Exception as e:
            # Set error flag on failure / Установка флага ошибки при неудаче
            self._internal_error_occurred = True
            self._lg.critical(f"Internal error: {e}.")


# ===== MAIN EXECUTION BLOCK / БЛОК ГЛАВНОГО ВЫПОЛНЕНИЯ =====
if __name__ == "__main__":
    # Test configuration creation / Тестирование создания конфигурации
    # This block is used for testing the AppConfig class functionality
    # Этот блок используется для тестирования функциональности класса AppConfig
    appcfg = AppConfig()
