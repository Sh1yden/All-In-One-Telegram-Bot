from sqlalchemy.orm import sessionmaker

from src.database.repositories.user_repository import UserRepository
from src.utils.db_utils import get_database_methods


def create_repositories(session_factory: sessionmaker) -> dict:
    """Factory function to create all repository instances."""
    db_methods = get_database_methods(session_factory)

    return {
        "user_repo": UserRepository(db_methods),
    }
