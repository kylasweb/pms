from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import ENUM

from src.database.sql import Base
from src.database.models.users import UserType

from src.database.constants import ID_LEN, NAME_LEN


class UserORM(Base):
    __tablename__ = 'users'

    user_id: str = Column(String(ID_LEN), primary_key=True, unique=True)
    is_tenant: bool = Column(Boolean)
    tenant_id: str = Column(String(ID_LEN), ForeignKey('tenants.tenant_id'))
    company_id: str = Column(String(ID_LEN))
    user_type: str = Column(ENUM(UserType), nullable=False)
    username: str = Column(String(NAME_LEN))
    password_hash: str = Column(String(255))
    email: str = Column(String(256))
    full_name: str = Column(String(NAME_LEN))
    contact_number: str = Column(String(13))

    def to_dict(self) -> dict[str, str | bool]:
        return {
            'user_id': self.user_id,
            'is_tenant': self.is_tenant,
            'tenant_id': self.tenant_id,
            'company_id': self.company_id,
            'user_type': self.user_type,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'contact_number': self.contact_number
        }
