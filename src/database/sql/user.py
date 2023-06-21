from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, inspect
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import relationship

from src.main import bcrypt
from src.database.sql import Base, engine
from src.database.models.users import UserType

from src.database.constants import ID_LEN, NAME_LEN


class UserORM(Base):
    __tablename__ = 'users'

    user_id: str = Column(String(ID_LEN), primary_key=True, unique=True)
    is_tenant: bool = Column(Boolean)
    tenant_id: str = Column(String(ID_LEN), ForeignKey('tenants.tenant_id'))
    username: str = Column(String(NAME_LEN))
    password_hash: str = Column(String(255))
    email: str = Column(String(256))
    full_name: str = Column(String(NAME_LEN))
    contact_number: str = Column(String(13))

    @classmethod
    def create_if_not_table(cls):
        if not inspect(engine).has_table(cls.__tablename__):
            Base.metadata.create_all(bind=engine)

    def __init__(self, user_id: str, is_tenant: bool, tenant_id: str, username: str, password: str,
                 email: str, full_name: str, contact_number: str):
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.is_tenant = is_tenant

        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email

    def __bool__(self) -> bool:
        return bool(self.user_id) and bool(self.username) and bool(self.email)

    def to_dict(self) -> dict[str, str | bool]:
        return {
            'user_id': self.user_id,
            'is_tenant': self.is_tenant,
            'tenant_id': self.tenant_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'contact_number': self.contact_number
        }




