import pickle
import redis
from typing import Any

from src.core import get_logger


class RedisCache:
    """Redis cache manager for data serialization and caching operations."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self._lg = get_logger()
        self._lg.debug("Initializing RedisCache.")

        self.connection = self._connect_to_redis(host, port, db)

    def _connect_to_redis(self, host: str, port: int, db: int) -> redis.Redis | None:
        """Connect to Redis server."""
        try:
            return redis.Redis(host=host, port=port, db=db)
        except Exception as e:
            self._lg.error(f"Failed to connect to Redis: {e}")
            return None

    def serialize_data(self, data: Any) -> bytes:
        """Serialize data using pickle."""
        try:
            return pickle.dumps(data)
        except Exception as e:
            self._lg.error(f"Failed to serialize data: {e}")
            raise

    def deserialize_data(self, data: bytes) -> Any:
        """Deserialize data using pickle."""
        try:
            return pickle.loads(data)
        except Exception as e:
            self._lg.error(f"Failed to deserialize data: {e}")
            return None

    def set(self, key: Any, data: Any) -> None:
        """Cache data in Redis."""
        try:
            serialized = self.serialize_data(data)
            self.connection.set(key, serialized)
            self._lg.debug(f"Successfully cached data for key: {key}")
        except Exception as e:
            self._lg.error(f"Failed to cache data for key {key}: {e}")

    def get(self, key: Any) -> Any:
        """Get cached data from Redis."""
        try:
            cached_data = self.connection.get(key)
            if cached_data and isinstance(cached_data, bytes):
                self._lg.debug(f"Successfully retrieved cached data for key: {key}")
                return self.deserialize_data(cached_data)
            else:
                self._lg.debug(f"No cached data found for key: {key}")
                return None
        except Exception as e:
            self._lg.error(f"Failed to get cached data for key {key}: {e}")
            return None

    def update(self, key: Any, updated_fields: dict[str, dict]) -> None:
        """
        Update specific fields in cached data.

        Args:
            key: Cache key
            updated_fields: Dict of {field: {"old": value, "new": value}}
        """
        try:
            cached_data = self.get(key)
            if cached_data is None:
                cached_data = {}

            for field, changes in updated_fields.items():
                cached_data[field] = changes["new"]

            self.set(key, cached_data)
            self._lg.debug(
                f"Updated cache for key {key}: {list(updated_fields.keys())}"
            )
        except Exception as e:
            self._lg.error(f"Failed to update cache for key {key}: {e}")

    def delete(self, key: Any) -> None:
        """Delete cached data."""
        try:
            self.connection.delete(key)
            self._lg.debug(f"Successfully deleted cached data for key: {key}")
        except Exception as e:
            self._lg.error(f"Failed to delete cached data for key {key}: {e}")

    def exists(self, key: Any) -> bool:
        """Check if key exists in cache."""
        try:
            return bool(self.connection.exists(key))
        except Exception as e:
            self._lg.error(f"Failed to check existence for key {key}: {e}")
            return False
