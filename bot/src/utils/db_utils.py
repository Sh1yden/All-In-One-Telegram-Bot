from aiogram.types import User

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, declarative_base

from bot.src.database.core import (
    SessionLocal,
    Base,
    engine,
    database_settings,
)
from bot.src.database import models
from bot.src.core import get_logger


class MethodsOfDatabase:
    """Universal methods sqlite and porstgresql."""

    def __init__(
        self,
        SessionLocal: sessionmaker,
        Base: declarative_base,
        engine: Engine | None,
        models: declarative_base,
    ):

        self._lg = get_logger()
        self._lg.debug("Logger init.")

        if engine is None:
            self._lg.critical("Engine is None!!! Error!")
            return

        self.session_local = SessionLocal()
        self.db = self.session_local
        self.base = Base
        self.engine = engine
        self.models = models

        self.create_tables_and_database()

    def create_tables_and_database(self) -> bool:
        """Main create database bot."""
        try:
            # TODO пока только sqlite, добавить потом posgresql.
            self._lg.debug(type(self.engine))
            self._lg.debug(f"Base из database.py: {id(self.base)}")

            # Создаем все таблицы которые есть в моделях
            # TODO возможно сделать как-то по другому?
            Base.metadata.create_all(self.engine)

            return True

        except Exception as e:
            self.db.rollback()
            self._lg.critical(f"Internal error: {e}.")
            return False
        finally:
            self._lg.debug("Database connection closed.")
            self.db.close()

    def create_one_user(
        self,
        model: declarative_base,
        user: User | None = None,
        *args,
        **kwargs,
    ) -> None:
        """
        Create one user.
        ## Table name: \n
        user_all_info \n
        ## All Columns: \n
        #### NOT NULL Columns:
        [ id ][ user_id ][ is_bot ][ first_name ] \n
        #### System column: \n
        [ id ] \n
        #### User data: \n
        [ user_id ][ is_bot ][ is_premium ][ language_code ][ supports_inline_queries ] \n
        \n
        #### User names: \n
        [ username ][ first_name ][ last_name ] \n
        #### Location data: \n
        [ device_type ][ city ][ latitude ][ longitude ]
        """
        # TODO ДАЙТЕ ДВА
        try:
            data = {}

            if user is not None:

                data = {
                    "user_id": getattr(user, "id", kwargs.get("user_id")),
                    "is_bot": getattr(user, "is_bot", kwargs.get("is_bot")),
                    "is_premium": getattr(user, "is_premium", kwargs.get("is_premium")),
                    "language_code": getattr(
                        user, "language_code", kwargs.get("language_code")
                    ),
                    "supports_inline_queries": getattr(
                        user,
                        "supports_inline_queries",
                        kwargs.get("supports_inline_queries", False),
                    ),
                    "username": getattr(user, "username", kwargs.get("username")),
                    "first_name": getattr(user, "first_name", kwargs.get("first_name")),
                    "last_name": getattr(user, "last_name", kwargs.get("last_name")),
                }

            data.update(kwargs)

            new_user_data = model(*args, **data)
            self.db.add(new_user_data)
            self.db.commit()
            self.db.refresh(new_user_data)

            self._lg.debug(f"Database create user successfully: {user}")

        except Exception as e:
            self.db.rollback()
            self._lg.error(f"Internal error: {e}.")
        finally:
            self._lg.debug("Database connection closed.")
            self.db.close()

    def delete_one_user_by_id(
        self,
        model: declarative_base,  # Модель, из которой удаляем (например, UserAllInfo)
        user_id: int,  # ID пользователя, которого нужно удалить
    ) -> bool | None:
        """Delete one user by id."""
        # TODO ДАЙТЕ ДВА
        try:
            if user_id is None:
                self._lg.error("user_id is required to delete a user.")
                return False  # или None, если предпочитаешь

            # Находим пользователя по ID
            user = self.db.query(model).filter(model.user_id == user_id).first()

            if user is None:
                self._lg.warning(f"User with user_id {user_id} not found for deletion.")
                return False  # Пользователь не найден, удаление не произошло

            # Удаляем объект из сессии
            self.db.delete(user)
            self.db.commit()

            self._lg.debug(f"Database delete user successfully: user_id={user_id}")
            return True  # Удаление прошло успешно

        except Exception as e:
            self.db.rollback()
            self._lg.error(f"Unexpected error during delete: {e}")
        finally:
            self._lg.debug("Database connection closed.")
            self.db.close()

    def update_one_user_by_id(self, model: declarative_base, id: int, **kwargs) -> None:
        """Update one user by id."""
        # TODO ДАЙТЕ ДВА
        try:
            user = self.db.query(model).filter(model.user_id == id).first()

            if user is None:
                self._lg.error("User is None!!!")
                return None

            if not kwargs:
                self._lg.warning("No fields provided to update.")
                return None

            # Обновляем поля, переданные в kwargs
            for key, value in kwargs.items():
                if hasattr(user, key):  # Проверяем, есть ли такое поле в модели
                    setattr(user, key, value)
                else:
                    self._lg.warning(
                        f"Field '{key}' does not exist on model {model.__name__}."
                    )

            self.db.commit()
            self.db.refresh(user)

            self._lg.debug(f"Database update user successfully: {user}")

            return user

        except Exception as e:
            self.db.rollback()
            self._lg.error(f"Internal error: {e}.")
        finally:
            self._lg.debug("Database connection closed.")
            self.db.close()

    def find_by_one_user_id(self, model: declarative_base, id: int) -> str | None:
        """Find one user by id."""
        # TODO ДАЙТЕ ДВА
        try:
            user = self.db.query(model).filter(model.user_id == id).first()

            return user

        except Exception as e:
            self.db.rollback()
            self._lg.error(f"Internal error: {e}.")
        finally:
            self._lg.debug("Database connection closed.")
            self.db.close()


def get_database_methods(session: sessionmaker) -> MethodsOfDatabase:
    dbm = MethodsOfDatabase(session, Base, engine, models)

    return dbm


if __name__ == "__main__":
    _lg = get_logger()
    dbm = get_database_methods(SessionLocal)

    _lg.debug(dbm.create_tables_and_database())
    _lg.debug(
        dbm.create_one_user(
            model=models.UserAllInfo,
            user_id=5080080714,
            is_bot=False,
            first_name="Shayden",
        )
    )
    _lg.debug(dbm.find_by_one_user_id(models.UserAllInfo, 5080080714))
    _lg.debug(
        dbm.update_one_user_by_id(models.UserAllInfo, 5080080714, is_premium=True)
    )
    _lg.debug(
        f"Database user deleted?: {dbm.delete_one_user_by_id(models.UserAllInfo, 5080080714)}"
    )
