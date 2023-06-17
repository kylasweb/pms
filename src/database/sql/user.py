from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import ENUM

from src.database.sql import Base
from src.database.models.users import UserType

from src.database.constants import ID_LEN, NAME_LEN


class User(Base):
    __tablename__ = 'users'

    user_id: str = Column(String(ID_LEN), primary_key=True, unique=True)
    is_tenant: bool = Column(Boolean)
    tenant_id: str = Column(String(ID_LEN), ForeignKey('tenants.tenant_id'))
    company_id: str = Column(String(ID_LEN))
    user_type: str = Column(ENUM(UserType), nullable=False)
    username: str = Column(String(NAME_LEN))
    email: str = Column(String(256))
    full_name: str = Column(String(NAME_LEN))
    contact_number: str = Column(String(13))
