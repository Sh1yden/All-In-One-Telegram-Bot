from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsSchema(BaseSettings):
    # TELEGRAM
    TELEGRAM_BOT_TOKEN: str
    # TG WEBHOOK
    TELEGRAM_WEBHOOK_SECRET: str

    # TUNA TUNNELS
    TUNA_TOKEN: str
    TUNA_API_TOKEN: str

    # SERVICES
    # VisualCrossing
    VISUAL_CROSSING_KEY: str
    # WeatherAPI
    WEATHER_API_KEY: str
    # OpenWeatherMap
    OPEN_WEATHER_MAP_API_KEY: str

    # Pydantic settings
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = SettingsSchema()  # type: ignore
