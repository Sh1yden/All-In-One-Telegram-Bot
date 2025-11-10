from pydantic import BaseModel


class UserSchema(BaseModel):
    # SYSTEM
    ID: int
    IS_BOT: bool
    IS_PREMIUM: bool | None = None
    SUPPORTS_INLINE_QUERIES: bool

    # NAME
    USERNAME: str | None = None
    FIRST_NAME: str
    LAST_NAME: str | None = None

    # FOR LOCATION
    DEVICE_TYPE: str
    CITY: str
    LATITUDE: int
    LONGITUDE: int

    # LANGUAGE
    LANGUAGE_CODE: str | None = None
