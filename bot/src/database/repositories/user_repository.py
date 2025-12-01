from typing import Any, Dict

from aiogram.types import User

from src.database.models import UserAllInfo
from src.database.repositories.base import BaseRepository
from src.utils.db_utils import MethodsOfDatabase


class UserRepository(BaseRepository[UserAllInfo]):
    """Repository for UserAllInfo entities."""

    def __init__(self, db_methods: MethodsOfDatabase):
        super().__init__(db_methods, UserAllInfo)

    def get_by_id(self, entity_id: int) -> Dict[str, Any] | None:
        """Get user by ID."""
        return self.db_methods.find_by_one_user_id(
            model=self.model, user_id=entity_id, as_dict=True
        )

    def save(self, entity_data: Dict[str, Any]) -> bool:
        """Save new user."""
        success, _ = self.db_methods.create_one_user(model=self.model, **entity_data)
        return success

    def save_from_telegram_user(self, user: User, **kwargs: Any) -> bool:
        """Save user from Telegram User object."""
        success, _ = self.db_methods.create_one_user(
            model=self.model, user=user, **kwargs
        )
        return success

    def update(self, entity_id: int, updates: Dict[str, Any]) -> bool:
        """Update user."""
        success, _, _ = self.db_methods.update_one_user_by_id(
            model=self.model, user_id=entity_id, **updates
        )
        return success

    def delete(self, entity_id: int) -> bool:
        """Delete user."""
        success, _ = self.db_methods.delete_one_user_by_id(
            model=self.model, user_id=entity_id
        )
        return success

    def exists(self, entity_id: int) -> bool:
        """Check if user exists."""
        return self.db_methods.user_exists(model=self.model, user_id=entity_id)

    def has_location(self, user_id: int) -> bool:
        """Check if user has location data."""
        return self.db_methods.user_location_exists(model=self.model, user_id=user_id)

    def update_location(
        self,
        user_id: int,
        city: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> bool:
        """Update user location."""
        updates = {}
        if city is not None:
            updates["city"] = city
        if latitude is not None:
            updates["latitude"] = latitude
        if longitude is not None:
            updates["longitude"] = longitude
        return self.update(user_id, updates)

    def get_all_user_ids(self) -> list[int]:
        """Get all user IDs."""
        return self.db_methods.get_all_user_ids(model=self.model)
