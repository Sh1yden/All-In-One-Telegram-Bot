import sys
from pathlib import Path

# Для прямого запуска файла
if __name__ == "__main__":
    # Добавляем bot/ в sys.path
    bot_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(bot_dir))

from typing import Type, Any, TypeVar

from aiogram.types import User

from sqlalchemy import Engine, inspect, exists, select, func
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from src.core import get_logger
from src.utils.cache import RedisCache

# TypeVar для generic типизации
T = TypeVar("T", bound=DeclarativeBase)


class MethodsOfDatabase:
    """Universal methods for SQLite and PostgreSQL."""

    def __init__(
        self,
        session_factory: sessionmaker,
        base: Type[DeclarativeBase],
        engine: Engine | None,
    ):
        """
        Initialize database methods

        Args:
            session_factory: SQLAlchemy session factory
            base: Declarative base class
            engine: Database engine
        """
        self._lg = get_logger()
        self._lg.debug("Initializing MethodsOfDatabase.")

        if engine is None:
            self._lg.critical("Engine is None!")
            raise ValueError("Database engine is required!")

        self.session_factory = session_factory
        self.base = base
        self.engine = engine
        self.cache = RedisCache()

        self.create_tables_and_database()

    def _get_session(self) -> Session:
        """
        Create new database session

        Returns:
            Session: New SQLAlchemy session
        """
        return self.session_factory()

    def create_tables_and_database(self) -> bool:
        """Create all database tables if they don't exist"""
        try:
            from src.database.models import UserAllInfo  # noqa: F401

            inspector = inspect(self.engine)
            existing_tables = inspector.get_table_names()

            if existing_tables:
                self._lg.debug(f"Found existing tables: {existing_tables}.")
            else:
                self._lg.debug("No existing tables found, creating...")

            # Создаём таблицы
            self.base.metadata.create_all(self.engine)

            # Проверяем
            new_tables = inspector.get_table_names()
            self._lg.debug(f"Database tables ready: {new_tables}.")

            return True

        except Exception as e:
            self._lg.critical(f"Failed to create tables: {e}.", exc_info=True)
            return False

    def create_one_user(
        self,
        model: Type[T],
        user: User | None = None,
        **kwargs: Any,
    ) -> tuple[bool, str]:
        """
        Create one user in database

        Args:
            model: Model class (e.g., UserAllInfo)
            user: Aiogram User object
            **kwargs: Additional fields to set

        Returns:
            tuple[bool, str]: (success, message)

        Example:
            success, msg = db.create_one_user(
                model=UserAllInfo,
                user=telegram_user,
                city="Moscow"
            )
        """
        session = self._get_session()
        try:
            # Проверка на существование
            user_id = user.id if user else kwargs.get("user_id")

            if user_id:
                existing = session.query(model).filter(model.user_id == user_id).first()  # type: ignore

                if existing:
                    self._lg.debug(f"User {user_id} already exists.")
                    return False, f"User {user_id} already exists."

            # Подготовка данных из User объекта
            data = {}
            if user is not None:
                data = {
                    "user_id": user.id,
                    "is_bot": user.is_bot,
                    "is_premium": user.is_premium,
                    "language_code": user.language_code,
                    "supports_inline_queries": getattr(
                        user, "supports_inline_queries", False
                    ),
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }

            # Добавляем/перезаписываем дополнительными параметрами
            data.update(kwargs)

            # Создание записи
            new_user = model(**data)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            # Redis cache
            self.cache.set(key=user_id, data=data)  # type: ignore

            self._lg.debug(f"User created: {new_user.user_id}.")  # type: ignore
            return True, f"User {new_user.user_id} created successfully."  # type: ignore

        except Exception as e:
            session.rollback()
            self._lg.error(f"Failed to create user: {e}.", exc_info=True)
            return False, f"Error: {str(e)}."
        finally:
            session.close()

    def delete_one_user_by_id(
        self,
        model: Type[T],
        user_id: int,
    ) -> tuple[bool, str]:
        """
        Delete one user by ID

        Args:
            model: Model class
            user_id: Telegram user ID

        Returns:
            tuple[bool, str]: (success, message)
        """
        session = self._get_session()
        try:
            user = session.query(model).filter(model.user_id == user_id).first()  # type: ignore

            if user is None:
                self._lg.warning(f"User {user_id} not found for deletion.")
                return False, f"User {user_id} not found."

            # Сохраняем данные для лога
            username = getattr(user, "username", "unknown")

            session.delete(user)
            session.commit()

            # Redis cache
            self.cache.delete(key=user_id)

            self._lg.debug(f"User deleted: {user_id} ({username}).")
            return True, f"User {user_id} deleted successfully."

        except Exception as e:
            session.rollback()
            self._lg.error(f"Failed to delete user {user_id}: {e}.", exc_info=True)
            return False, f"Error: {str(e)}"
        finally:
            session.close()

    def update_one_user_by_id(
        self,
        model: Type[T],
        user_id: int,
        **kwargs: Any,
    ) -> tuple[bool, str, dict[str, Any] | None]:
        """
        Update one user by ID

        Args:
            model: Model class
            user_id: Telegram user ID
            **kwargs: Fields to update

        Returns:
            tuple[bool, str, dict]: (success, message, updated_fields)

        Example:
            success, msg, changes = db.update_one_user_by_id(
                model=UserAllInfo,
                user_id=123456,
                first_name="New Name",
                city="Moscow"
            )
        """
        session = self._get_session()
        try:
            user = session.query(model).filter(model.user_id == user_id).first()  # type: ignore

            if user is None:
                self._lg.warning(f"User {user_id} not found for update.")
                return False, f"User {user_id} not found.", None

            if not kwargs:
                self._lg.warning("No fields provided for update.")
                return False, "No fields to update.", None

            updated_fields = {}
            invalid_fields = []

            # Обновляем только изменённые поля
            for key, value in kwargs.items():
                if hasattr(user, key):
                    old_value = getattr(user, key)
                    if old_value != value:
                        setattr(user, key, value)
                        updated_fields[key] = {"old": old_value, "new": value}
                else:
                    invalid_fields.append(key)

            if invalid_fields:
                self._lg.warning(f"Invalid fields ignored: {invalid_fields}.")

            if not updated_fields:
                return True, "No changes detected.", {}

            session.commit()
            session.refresh(user)

            # Redis cache
            self.cache.update(user_id, updated_fields)

            self._lg.debug(f"User {user_id} updated: {list(updated_fields.keys())}.")
            return True, f"Updated {len(updated_fields)} fields.", updated_fields

        except Exception as e:
            session.rollback()
            self._lg.error(f"Failed to update user {user_id}: {e}.", exc_info=True)
            return False, f"Error: {str(e)}", None
        finally:
            session.close()

    def user_exists(self, model: Type[T], user_id: int) -> bool:
        """
        Check if user exists in database

        Args:
            model: Model class
            user_id: Telegram user ID

        Returns:
            bool: True if user exists, False otherwise
        """
        session = self._get_session()
        try:
            if self.cache.exists(user_id):
                return True
            else:
                # Используем EXISTS для оптимизации
                stmt = select(exists().where(model.user_id == user_id))  # type: ignore
                result = session.execute(stmt).scalar()

                return bool(result)

        except Exception as e:
            self._lg.error(f"Error checking user existence: {e}.")
            return False
        finally:
            session.close()

    def user_location_exists(self, model: Type[T], user_id: int) -> bool:
        """
        Check if user location exists in database

        Args:
            model: Model class
            user_id: Telegram user ID

        Returns:
            bool: True if user location exists, False otherwise
        """
        session = self._get_session()
        try:
            cached_data = self.cache.get(user_id)

            if cached_data:
                self._lg.debug(f"Cached data (deserialized) - {cached_data}")

                if cached_data and isinstance(cached_data, dict):
                    city = cached_data.get("city")
                    lat = cached_data.get("latitude")
                    lon = cached_data.get("longitude")

                    if city or lat or lon:
                        self._lg.debug(
                            f"User {user_id} location found in cache: city={city}, lat={lat}, lon={lon}"
                        )
                        return True

                    self._lg.debug(f"User {user_id} location not found in cache")
                    return False
                else:
                    self._lg.debug("Cached data not isinstance!!!")
                    return False

            else:
                self._lg.debug(f"No cache for user {user_id}, checking database")
                user = session.query(model).filter(model.user_id == user_id).first()  # type: ignore

                if not user:
                    self._lg.warning(f"User {user_id} not found in database")
                    return False

                city = getattr(user, "city", None)
                lat = getattr(user, "latitude", None)
                lon = getattr(user, "longitude", None)

                if city or lat or lon:
                    self._lg.debug(
                        f"User {user_id} location found in DB: city={city}, lat={lat}, lon={lon}"
                    )
                    return True

                self._lg.debug(f"User {user_id} location not found in DB")
                return False

        except Exception as e:
            self._lg.error(f"Error checking user existence: {e}.")
            return False
        finally:
            session.close()

    def find_by_one_user_id(
        self,
        model: Type[T],
        user_id: int,
        as_dict: bool = True,
    ) -> T | dict[str, Any] | None:
        """
        Find one user by ID

        Args:
            model: Model class
            user_id: Telegram user ID
            as_dict: Return as dictionary instead of model instance

        Returns:
            Model instance, dictionary, or None if not found
        """
        session = self._get_session()
        try:
            cached_data = self.cache.get(user_id)

            if cached_data:
                return cached_data

            else:
                user = session.query(model).filter(model.user_id == user_id).first()  # type: ignore

                if user is None:
                    self._lg.debug(f"User {user_id} not found.")
                    return None

                if as_dict:
                    # Преобразуем в словарь
                    result = {
                        column.name: getattr(user, column.name)
                        for column in model.__table__.columns
                    }
                    self._lg.debug(f"User {user_id} found and returned as dict.")
                    return result
                else:
                    # Отвязываем от сессии
                    session.expunge(user)
                    self._lg.debug(f"User {user_id} found and returned as object.")
                    return user

        except Exception as e:
            self._lg.error(f"Error finding user {user_id}: {e}.")
            return None
        finally:
            session.close()

    def find_users(  # TODO
        self,
        model: Type[T],
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        as_dict: bool = True,
    ) -> list[dict[str, Any]] | list[T]:
        """
        Find multiple users with filters

        Args:
            model: Model class
            filters: Dictionary of field:value pairs for filtering
            limit: Maximum number of results
            offset: Skip first N results
            as_dict: Return as list of dictionaries

        Returns:
            List of users (as dicts or model instances)

        Example:
            users = db.find_users(
                model=UserAllInfo,
                filters={"is_premium": True, "language_code": "ru"},
                limit=50
            )
        """
        session = self._get_session()
        try:
            query = session.query(model)

            # Применяем фильтры
            if filters:
                for key, value in filters.items():
                    if hasattr(model, key):
                        query = query.filter(getattr(model, key) == value)
                    else:
                        self._lg.warning(f"Invalid filter field: {key}.")

            # Применяем лимиты
            query = query.limit(limit).offset(offset)

            users = query.all()

            self._lg.debug(f"Found {len(users)} users with filters: {filters}.")

            if as_dict:
                return [
                    {
                        col.name: getattr(user, col.name)
                        for col in model.__table__.columns
                    }
                    for user in users
                ]
            else:
                # Отвязываем от сессии
                for user in users:
                    session.expunge(user)
                return users

        except Exception as e:
            self._lg.error(f"Error finding users: {e}.", exc_info=True)
            return []
        finally:
            session.close()

    def count_users(  # TODO
        self,
        model: Type[T],
        filters: dict[str, Any] | None = None,
    ) -> int:
        """
        Count users with optional filters

        Args:
            model: Model class
            filters: Dictionary of field:value pairs for filtering

        Returns:
            int: Number of users matching filters

        Example:
            premium_count = db.count_users(
                model=UserAllInfo,
                filters={"is_premium": True}
            )
        """
        session = self._get_session()
        try:
            query = session.query(func.count(model.id))  # type: ignore

            if filters:
                for key, value in filters.items():
                    if hasattr(model, key):
                        query = query.filter(getattr(model, key) == value)

            count = query.scalar()

            self._lg.debug(f"Count: {count} users with filters: {filters}.")

            return count or 0

        except Exception as e:
            self._lg.error(f"Error counting users: {e}.")
            return 0
        finally:
            session.close()

    def create_many_users(  # TODO
        self,
        model: Type[T],
        users_data: list[dict[str, Any]],
    ) -> tuple[int, int, list[str]]:
        """
        Create multiple users at once (batch operation)

        Args:
            model: Model class
            users_data: List of dictionaries with user data

        Returns:
            tuple[int, int, list]: (created_count, failed_count, error_messages)

        Example:
            created, failed, errors = db.create_many_users(
                model=UserAllInfo,
                users_data=[
                    {"user_id": 1, "first_name": "User1", "is_bot": False},
                    {"user_id": 2, "first_name": "User2", "is_bot": False},
                ]
            )
        """
        session = self._get_session()
        created = 0
        failed = 0
        errors = []

        try:
            for user_data in users_data:
                try:
                    new_user = model(**user_data)
                    session.add(new_user)
                    created += 1
                except Exception as e:
                    error_msg = f"Failed to add user {user_data.get('user_id')}: {e}"
                    self._lg.warning(error_msg)
                    errors.append(error_msg)
                    failed += 1

            session.commit()

            self._lg.debug(f"Batch creation: {created} users created, {failed} failed.")

            return created, failed, errors

        except Exception as e:
            session.rollback()
            self._lg.error(f"Batch creation failed: {e}.", exc_info=True)
            return 0, len(users_data), [f"Batch error: {str(e)}"]
        finally:
            session.close()

    def get_all_user_ids(  # TODO
        self,
        model: Type[T],
    ) -> list[int]:
        """
        Get list of all user IDs

        Args:
            model: Model class

        Returns:
            list[int]: List of user IDs
        """
        session = self._get_session()
        try:
            user_ids = session.query(model.user_id).all()  # type: ignore
            result = [user_id[0] for user_id in user_ids]

            self._lg.debug(f"Retrieved {len(result)} user IDs.")
            return result

        except Exception as e:
            self._lg.error(f"Error getting user IDs: {e}.")
            return []
        finally:
            session.close()

    def close(self) -> None:
        """
        Close database engine and dispose connection pool

        Should be called when shutting down the application
        """
        try:
            self.engine.dispose()
            self._lg.debug("Database engine disposed.")
        except Exception as e:
            self._lg.error(f"Error disposing engine: {e}.")


def get_database_methods(session_factory: sessionmaker) -> MethodsOfDatabase:
    """Factory function to create MethodsOfDatabase instance"""
    from src.database.core import Base, engine

    return MethodsOfDatabase(session_factory, Base, engine)


if __name__ == "__main__":
    """Тестирование методов базы данных"""
    from src.database.core import SessionLocal
    from src.database.models import UserAllInfo

    _lg = get_logger()

    _lg.debug("Testing MethodsOfDatabase:")

    # Создаём экземпляр
    dbm = get_database_methods(SessionLocal)

    # # Тест 1: Создание пользователя
    # _lg.debug("Test 1: Creating user:")
    # success, msg = dbm.create_one_user(
    #     model=UserAllInfo,
    #     user_id=5080080714,
    #     is_bot=False,
    #     first_name="Shayden",
    #     supports_inline_queries=False,
    # )
    # _lg.debug(f"Result: {success} - {msg}.")

    # Тест 2: Проверка существования
    _lg.debug("Test 2: Check if user exists:")
    exists = dbm.user_exists(UserAllInfo, 5080080714)
    _lg.debug(f"User exists: {exists}.")

    # Тест 2.1: Проверка существования локации
    _lg.debug("Test 2.1: Check if user location exists:")
    loc_exists = dbm.user_location_exists(UserAllInfo, 5080080714)
    _lg.debug(f"User location exists: {loc_exists}.")

    # Тест 3: Поиск пользователя
    _lg.debug("Test 3: Find user:")
    user = dbm.find_by_one_user_id(UserAllInfo, 5080080714, as_dict=True)
    _lg.debug(f"Found user: {user}.")

    # Тест 4: Обновление
    # _lg.debug("Test 4: Update user:")
    # success, msg, changes = dbm.update_one_user_by_id(
    #     UserAllInfo, 5080080714, is_premium=True, city="Moscow"
    # )
    # _lg.debug(f"Result: {success} - {msg}.")
    # _lg.debug(f"Changes: {changes}.")

    # Тест 5: Подсчёт
    _lg.debug("Test 5: Count users:")
    count = dbm.count_users(UserAllInfo)
    _lg.debug(f"Total users: {count}.")

    # Тест 6: Удаление
    # _lg.debug("Test 6: Delete user:")
    # success, msg = dbm.delete_one_user_by_id(UserAllInfo, 5080080714)
    # _lg.debug(f"Result: {success} - {msg}.")

    # Закрываем соединение
    dbm.close()

    _lg.debug("Testing completed!")
