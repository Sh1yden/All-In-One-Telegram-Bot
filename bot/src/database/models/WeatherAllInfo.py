from sqlalchemy import Column, Integer, String

from src.database.core.database import Base


class WeatherAllInfo(Base):
    """
    ## Table name: \n
    weather_all_info \n
    """  # TODO

    __tablename__ = "weather_all_info"
    __table_args__ = {"extend_existing": True}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,  # NOT NULL
    )

    weather_id = Column(String, nullable=False)

    weather_now_msg = Column(String)
    weather_hours_msg = Column(String)
    weather_day_night_msg = Column(String)
    weather_5d_msg = Column(String)
    weather_rain_msg = Column(String)
    weather_wind_pressure_msg = Column(String)

    def __repr__(self):
        return f"<Weather(weather_id={self.weather_id}, weather_now_msg='{self.weather_now_msg})'>"
