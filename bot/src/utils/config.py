from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsSchema(BaseSettings):
    # TELEGRAM
    TELEGRAM_BOT_TOKEN: str

    # PGSQL
    PG_USERNAME: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: str
    PG_DB_NAME: str
    PG_DB_ROOT_NAME: str

    # TUNA TUNNELS
    TUNA_TOKEN: str
    TUNA_API_TOKEN: str

    # Pydantic settings
    model_config = SettingsConfigDict(env_file=".env")


settings = SettingsSchema()  # type: ignore
