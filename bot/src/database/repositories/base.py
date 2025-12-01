from abc import ABC, abstractmethod
from typing import Type, Any, TypeVar, Generic

from sqlalchemy.orm import DeclarativeBase

from src.core import get_logger
from src.utils.db_utils import MethodsOfDatabase

T = TypeVar("T", bound=DeclarativeBase)


class BaseRepository(ABC, Generic[T]):
    """Base repository class providing common database operations."""

    def __init__(self, db_methods: MethodsOfDatabase, model: Type[T]):
        self._lg = get_logger()
        self.db_methods = db_methods
        self.model = model

    @abstractmethod
    def get_by_id(self, entity_id: Any) -> T | dict[str, Any] | None:
        """Get entity by ID."""
        pass

    @abstractmethod
    def save(self, entity_data: dict[str, Any]) -> bool:
        """Save new entity."""
        pass

    @abstractmethod
    def update(self, entity_id: Any, updates: dict[str, Any]) -> bool:
        """Update entity."""
        pass

    @abstractmethod
    def delete(self, entity_id: Any) -> bool:
        """Delete entity."""
        pass

    @abstractmethod
    def exists(self, entity_id: Any) -> bool:
        """Check if entity exists."""
        pass

    def find_all(
        self, filters: dict[str, Any] | None = None, limit: int = 100, offset: int = 0
    ) -> list[dict[str, Any]]:
        """Find multiple entities with filters."""
        return self.db_methods.find_users(
            model=self.model, filters=filters, limit=limit, offset=offset, as_dict=True
        )  # type: ignore

    def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count entities with filters."""
        return self.db_methods.count_users(model=self.model, filters=filters)
