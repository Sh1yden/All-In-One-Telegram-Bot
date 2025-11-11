from sqlalchemy import Engine, create_engine

from bot.src.utils import SettingsSchema
from bot.src.core import get_logger


_lg = get_logger()


class DataBaseSettingsSchema(SettingsSchema):
    # DATABASES
    DATABASE_STATUS: str

    # SQLITE
    SQLITE_DB_URL: str

    # PGSQL
    PG_USERNAME: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: str
    PG_DB_NAME: str
    PG_DB_ROOT_NAME: str


database_settings = DataBaseSettingsSchema()  # type: ignore


def get_engine(db_status=database_settings.DATABASE_STATUS) -> Engine | None:
    try:
        if db_status == "development":
            return create_engine(database_settings.SQLITE_DB_URL + "dev.db")
        elif db_status == "product":
            return create_engine(database_settings.PG_HOST)
    except Exception as e:
        _lg.error(f"Internal error: {e}.")
