from sqlalchemy import Column, String, Boolean, DateTime

from src.database.constants import ID_LEN
from src.database.sql import Base


class NotificationORM(Base):
    __tablename__ = 'notifications'
    id = Column(String(ID_LEN), primary_key=True)
    user_id = Column(String(ID_LEN))
    title = Column(String(ID_LEN))
    message = Column(String(ID_LEN))
    category = Column(String(ID_LEN))
    time_read = Column(DateTime, nullable=True)
    is_read = Column(Boolean)
    time_created = Column(DateTime)

