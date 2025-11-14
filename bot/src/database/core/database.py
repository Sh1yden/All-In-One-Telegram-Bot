from sqlalchemy.orm import sessionmaker, declarative_base

from .database_config import get_engine
from bot.src.core import get_logger

_lg = get_logger()

engine = get_engine()
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)
Base = declarative_base()

_lg.debug(type(engine))
_lg.debug(f"Base из database.py: {id(Base)}")
