from typing import Any, Dict

from src.database.models import WeatherAllInfo
from src.database.repositories.base import BaseRepository
from src.utils.db_utils import MethodsOfDatabase


class WeatherRepository(BaseRepository[WeatherAllInfo]):
    """Repository for WeatherAllInfo entities."""

    def __init__(self, db_methods: MethodsOfDatabase):
        super().__init__(db_methods, WeatherAllInfo)

    def get_by_id(self, entity_id: int) -> Dict[str, Any] | None:
        """Get weather cache by ID."""
        return self.db_methods.find_weather_cache_by_id(
            model=self.model, weather_id=entity_id, as_dict=True
        )

    def save(self, entity_data: Dict[str, Any]) -> bool:
        """Save new weather cache."""
        success, _ = self.db_methods.create_weather_cache(
            model=self.model, **entity_data
        )
        return success

    def save_from_weather_id(self, weather_id, **kwargs: Any) -> bool:
        """Save new weather cache from weather_id."""
        success, _ = self.db_methods.create_weather_cache(
            model=self.model, weather_id=weather_id, **kwargs
        )
        return success

    def update(self, entity_id: Any, updates: Dict[str, Any]) -> bool:
        return super().update(entity_id, updates)

    def delete(self, entity_id: int) -> bool:
        """Delete weather cache."""
        success, _ = self.db_methods.delete_weather_cache_by_id(
            model=self.model, weather_id=entity_id
        )
        return success

    def exists(self, entity_id: int) -> bool:
        """Check if weather cache exists."""
        return self.db_methods.weather_cache_exists(
            model=self.model, weather_id=entity_id
        )
