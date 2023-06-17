from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from datetime import date
from src.database.constants import ID_LEN, NAME_LEN
from src.database.sql import Base


class TenantORM(Base):
    __tablename__ = 'tenants'

    tenant_id: str = Column(String(ID_LEN), primary_key=True)
    name: str = Column(String(NAME_LEN))
    email: str = Column(String(256))
    phone_number: str = Column(String(13))
    address_id: str = Column(String(ID_LEN))
    lease_start_date: date = Column(Date)
    lease_end_date: date = Column(Date)
