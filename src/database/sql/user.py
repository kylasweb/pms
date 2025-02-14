from sqlalchemy import Column, String, Boolean, ForeignKey, inspect

from src.database.constants import ID_LEN, NAME_LEN
from src.database.sql import Base, engine


class UserORM(Base):
    __tablename__ = 'users'

    user_id: str = Column(String(ID_LEN), primary_key=True, unique=True)
    is_tenant: bool = Column(Boolean, default=False)
    tenant_id: str = Column(String(ID_LEN), ForeignKey('tenants.tenant_id'))
    username: str = Column(String(NAME_LEN))
    password_hash: str = Column(String(255))
    email: str = Column(String(256))
    full_name: str = Column(String(NAME_LEN))
    contact_number: str = Column(String(13))
    account_verified: bool = Column(Boolean, default=False)

    @classmethod
    def create_if_not_table(cls):
        if not inspect(engine).has_table(cls.__tablename__):
            Base.metadata.create_all(bind=engine)

    def __init__(self, user_id: str, is_tenant: bool, tenant_id: str, username: str, password_hash: str,
                 email: str, full_name: str, contact_number: str):
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.is_tenant = is_tenant
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.full_name = full_name
        self.contact_number = contact_number

    def __bool__(self) -> bool:
        return bool(self.user_id) and bool(self.username) and bool(self.email)

    def to_dict(self) -> dict[str, str | bool]:
        return {
            'user_id': self.user_id,
            'is_tenant': self.is_tenant,
            'tenant_id': self.tenant_id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'full_name': self.full_name,
            'contact_number': self.contact_number
        }




