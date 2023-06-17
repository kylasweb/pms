from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, inspect
from datetime import date
from src.database.constants import ID_LEN, NAME_LEN
from src.database.sql import Base, engine


class TenantORM(Base):
    __tablename__ = 'tenants'

    tenant_id: str = Column(String(ID_LEN), primary_key=True)
    address_id: str = Column(String(ID_LEN), ForeignKey('addresses.address_id'))
    name: str = Column(String(NAME_LEN))
    email: str = Column(String(256))
    phone_number: str = Column(String(13))
    lease_start_date: date = Column(Date)
    lease_end_date: date = Column(Date)


    @classmethod
    def create_if_not_table(cls):
        if not inspect(engine).has_table(cls.__tablename__):
            Base.metadata.create_all(bind=engine)
