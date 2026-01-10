from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.utils import SettingsSchema


class DataBaseSettingsSchema(SettingsSchema):
    # DATABASES
    DATABASE_STATUS: str

    # SQLITE
    SQLITE_DB_URL: str

    # PGSQL
    POSTGRES_HOST: str
    POSTGRES_ASYNCPG: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: str


database_settings = DataBaseSettingsSchema()  # type: ignore


async def get_engine(db_status=database_settings.DATABASE_STATUS) -> AsyncEngine | None:
    """
    Create async database engine

    Args:
        db_status: Database status ('development' or 'product')

    Returns:
        AsyncEngine: Async SQLAlchemy engine
    """
    from src.core import get_logger

    _lg = get_logger()
    try:
        if db_status == "development":
            _lg.debug(f"Using SQLite: {database_settings.SQLITE_DB_URL}")
            return create_async_engine(database_settings.SQLITE_DB_URL)

        elif db_status == "product":
            _lg.debug(f"=== PostgreSQL Connection Details ===")
            _lg.debug(f"ASYNCPG: {database_settings.POSTGRES_ASYNCPG}")
            _lg.debug(f"Host: {database_settings.POSTGRES_HOST}")
            _lg.debug(f"Port: {database_settings.POSTGRES_PORT}")
            _lg.debug(f"Database: {database_settings.POSTGRES_DB}")
            _lg.debug(f"User: {database_settings.POSTGRES_USER}")

            return create_async_engine(
                f"postgresql+"
                f"{database_settings.POSTGRES_ASYNCPG}"
                f"://{database_settings.POSTGRES_USER}:"
                f"{database_settings.POSTGRES_PASSWORD}@"
                f"{database_settings.POSTGRES_HOST}:"
                f"{database_settings.POSTGRES_PORT}/"
                f"{database_settings.POSTGRES_DB}"
            )

        else:
            _lg.error(f"Unknown database status: {db_status}")
            raise ValueError(f"Unknown database status: {db_status}")
    except Exception as e:
        _lg.error(f"Internal error: {e}.")


if __name__ == "__main__":
    print(
        f"postgresql+"
        f"{database_settings.POSTGRES_ASYNCPG}"
        f"://{database_settings.POSTGRES_USER}:"
        f"{database_settings.POSTGRES_PASSWORD}@"
        f"{database_settings.POSTGRES_HOST}:"
        f"{database_settings.POSTGRES_PORT}/"
        f"{database_settings.POSTGRES_DB}"
    )
