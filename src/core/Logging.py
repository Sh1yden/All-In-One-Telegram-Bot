import logging
import os
import json
import datetime
import inspect


# ANSI цвета для терминала
class Colors:
    # Снять цвет
    RESET = "\033[0m"

    # CONSOLE LOG
    CURRENT_TIME_COLOR = "\u001b[34;1m"  # Светло синий
    FILENAME_COLOR = "\u001b[32m"  # Зелёный
    MODULE_COLOR = "\u001b[33m"  # Желтый
    CLASS_COLOR = "\u001b[34m"  # Голубой
    DEF_COLOR = "\u001b[36m"  # Синий
    MESSAGE_COLOR = "\u001b[37m"  # Белый

    # LOG LVL
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    BRIGHT_RED = "\033[91m"


class JSONFormatter(logging.Formatter):
    """Кастомный форматтер для логов в формате JSON"""

    def format(self, record) -> str:

        stack = inspect.stack()
        caller_frame = stack[2].frame

        # Получаем имя файла без пути
        current_time = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        level = record.levelname
        filename = os.path.basename(record.pathname) if record.pathname else None
        module = inspect.getmodule(
            caller_frame
        ).__name__  # pyright: ignore[reportOptionalMemberAccess]
        cls_obj = caller_frame.f_locals.get("self", None)
        cls_name = cls_obj.__class__.__name__ if cls_obj else None
        deff = record.funcName
        message = record.getMessage()

        # Формируем JSON структуру
        log_entry = {
            "timestamp": current_time,
            "level": level,
            "filename": filename,
            "module": module,
            "class": cls_name,
            "def": deff,
            "message": message,
        }

        return json.dumps(log_entry, ensure_ascii=False)


class ColoredConsoleFormatter(logging.Formatter):
    """Кастомный форматтер для цветного вывода в консоль"""

    def format(self, record):

        stack = inspect.stack()
        caller_frame = stack[2].frame

        # Получаем имя файла без пути
        current_time = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        level = record.levelname
        filename = os.path.basename(record.pathname) if record.pathname else None

        # Сопоставление уровней с цветами
        self.LEVEL_COLORS = {
            "DEBUG": Colors.CYAN,
            "INFO": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "CRITICAL": Colors.BRIGHT_RED,
        }
        # Получаем цвет для уровня
        color = self.LEVEL_COLORS.get(record.levelname, Colors.RESET)

        module = inspect.getmodule(
            caller_frame
        ).__name__  # pyright: ignore[reportOptionalMemberAccess]
        cls_obj = caller_frame.f_locals.get("self", None)
        cls_name = cls_obj.__class__.__name__ if cls_obj else None
        deff = record.funcName
        message = record.getMessage()

        # Цветной формат для консоли
        colored_output = (
            f"{Colors.CURRENT_TIME_COLOR}{current_time}{Colors.RESET} | "
            f"{color}{level:<8}{Colors.RESET} | "
            f"{Colors.FILENAME_COLOR}{filename}{Colors.RESET} | "
            f"{Colors.MODULE_COLOR}{module}{Colors.RESET} | "
            f"{Colors.CLASS_COLOR}{cls_name}{Colors.RESET} | "
            f"{Colors.DEF_COLOR}{deff}{Colors.RESET} | "
            f"{message}"
        )

        return colored_output


def setup_logging():
    """
    Настройка логирования в консоль (с цветами) и файлы в формате JSONL
    """

    # Создаем логгер
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Очищаем существующие обработчики
    logger.handlers.clear()

    # === Обработчик для консоли с цветами ===
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = ColoredConsoleFormatter()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # === Обработчик для файлов в формате JSON ===
    # Генерируем имя файла с текущей датой и номером
    today = datetime.date.today()
    file_number = 1
    while True:
        log_filename = f"{today.strftime('%Y-%m-%d')}-{file_number:02d}.jsonl"
        log_filepath = os.path.join("logs", log_filename)
        if not os.path.exists(log_filepath):
            break
        file_number += 1

    file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    json_formatter = JSONFormatter()
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)

    return logger


# Глобальный логгер для всего приложения
app_logger = None


def get_logger():
    """Получение настроенного логгера."""
    global app_logger
    if app_logger is None:
        app_logger = setup_logging()
    return app_logger


# Пример использования
if __name__ == "__main__":
    # Настройка логирования
    logger = get_logger()

    # Тестовые сообщения
    logger.debug("Debug message test / Тест отладочного сообщения")
    logger.info("Info message test / Тест информационного сообщения")
    logger.warning("Warning message test / Тест предупреждающего сообщения")
    logger.error("Error message test / Тест сообщения об ошибке")
    logger.critical("Critical message test / Тест критического сообщения")

    # Пример логирования с переменными
    user_id = 12345
    logger.info(f"User {user_id} logged in")
