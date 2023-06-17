from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from datetime import date
from src.database.constants import ID_LEN, NAME_LEN
from src.database.sql import Base


class AddressORM(Base):
    __tablename__ = 'addresses'

    address_id = Column(String(ID_LEN), primary_key=True)
    street = Column(String(NAME_LEN), index=True)
    city = Column(String(NAME_LEN), index=True)
    state = Column(String(NAME_LEN), index=True)
    postal_code = Column(String(8))
    country = Column(String(NAME_LEN))
