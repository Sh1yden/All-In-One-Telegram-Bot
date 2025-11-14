from bot.src.database.core import SessionLocal, Base, engine
from bot.src.database import models
import time

from src.core import get_logger

_lg = get_logger()

db = SessionLocal()

_lg.debug(type(engine))
_lg.debug(f"Base из database.py: {id(Base)}")

# Создаем таблицы
Base.metadata.create_all(engine)

start_time = time.time()

# * NEW VALUES
new_user = models.UserAllInfo(
    user_id=123456,
    is_bot=False,
    supports_inline_queries=True,
    first_name="Shayden",
)

# * ADD NEW VALUES
db.add(new_user)
db.commit()

end_time = time.time()

_lg.debug(f"Time of run add to database - {end_time - start_time}")

# * QUERY
user = db.query(models.UserAllInfo).filter(models.UserAllInfo.user_id == 123456).first()
print(user)

db.close()
