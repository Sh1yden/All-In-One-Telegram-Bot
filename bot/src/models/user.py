from pydantic import BaseModel


class UserSchema(BaseModel):
    # GENERAL
    ID: int
    USERNAME: str | None = None
    FIRST_NAME: str
    LAST_NAME: str | None = None
    IS_PREMIUM: bool | None = None

    # FOR LOCATION
    DEVICE_TYPE: str
    CITY: str
    LATITUDE: int
    LONGITUDE: int

    # LANGUAGE
    LANGUAGE_CODE: str | None = None
