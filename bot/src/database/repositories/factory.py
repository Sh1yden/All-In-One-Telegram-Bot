from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.repositories.user_repository import UserRepository
from src.database.repositories.weather_repository import WeatherRepository
from src.database.core import init_database
from src.utils.db_utils import get_database_methods
from src.database.core.database import Base


async def create_repositories(session_factory: async_sessionmaker) -> dict:
    """Factory function to create all repository instances."""
    # Инициализация БД
    engine, SessionLocal = await init_database()

    db_methods = await get_database_methods(SessionLocal, Base, engine)

    return {
        "user_repo": UserRepository(db_methods),
        "weather_repo": WeatherRepository(db_methods),
    }
