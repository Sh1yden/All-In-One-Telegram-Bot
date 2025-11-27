from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsSchema(BaseSettings):
    # TELEGRAM
    TELEGRAM_BOT_TOKEN: str
    # TG WEBHOOK
    TELEGRAM_WEBHOOK_SECRET: str

    # TUNA TUNNELS
    TUNA_TOKEN: str
    TUNA_API_TOKEN: str

    # Pydantic settings
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = SettingsSchema()  # type: ignore
