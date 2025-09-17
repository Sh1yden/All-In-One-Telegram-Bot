"""Сервис для работы с погодными данными."""


class WeatherService:
    """Сервис для получения данных о погоде."""

    @staticmethod
    async def get_current_weather(city: str = "Москва") -> str:
        """Получить текущую погоду для города."""
        # Здесь будет обращение к погодному API
        # Например OpenWeatherMap, WeatherAPI и т.д.

        return f"🌤 Погода в городе {city}:\nТемпература: 22°C\nВлажность: 65%\nВетер: 5 м/с"

    @staticmethod
    async def get_loading_message() -> str:
        """Получить сообщение загрузки."""
        return "🔄 Получаю данные о погоде..."
