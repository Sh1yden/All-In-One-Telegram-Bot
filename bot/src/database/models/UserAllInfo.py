from sqlalchemy import Column, Integer, BigInteger, String, Boolean

from src.database.core.database import Base


class UserAllInfo(Base):
    """
    ## Table name: \n
    user_all_info \n
    ## All Columns: \n
    #### NOT NULL Columns:
    [ id ][ user_id ][ is_bot ][ first_name ] \n
    #### System column: \n
    [ id ] \n
    #### User data: \n
    [ user_id ][ is_bot ][ is_premium ][ language_code ][ supports_inline_queries ] \n
    \n
    #### User names: \n
    [ username ][ first_name ][ last_name ] \n
    #### Location data: \n
    [ device_type ][ city ][ latitude ][ longitude ]
    """

    __tablename__ = "user_all_info"
    __table_args__ = {"extend_existing": True}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,  # NOT NULL
    )

    user_id = Column(BigInteger, nullable=False)
    is_bot = Column(Boolean, nullable=False)
    is_premium = Column(Boolean)
    language_code = Column(String)
    supports_inline_queries = Column(Boolean, nullable=True)

    username = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String)

    device_type = Column(String)
    city = Column(String)
    latitude = Column(String)
    longitude = Column(String)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, first_name='{self.first_name})'>"
