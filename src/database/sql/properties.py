from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from datetime import date
from src.database.constants import ID_LEN
from src.database.sql import Base


class PropertyORM(Base):
    __tablename__ = 'properties'

    property_id = Column(String(ID_LEN), primary_key=True)
    address_id = Column(String(ID_LEN), ForeignKey('address.address_id'))
    property_type = Column(String)
    number_of_units = Column(Integer)
    available_units: int = Column(Integer)
    amenities: list[str] = Column()
    landlord: str = Column(String(64))
    maintenance_contact: str = Column(String(64))
    lease_terms: str = Column(Text)
    description: str = Column(Text)
    built_year: int = Column(Integer)
    parking_spots: int = Column(Integer)


class UnitORM(Base):
    __tablename__ = 'units'

    unit_id: str = Column(String(ID_LEN), primary_key=True)
    property_id: str = Column(String(ID_LEN), ForeignKey('properties.property_id'))
    tenant_id: str = Column(String(ID_LEN), ForeignKey('tenants.tenant_id'))
    is_occupied: bool = Column(Boolean)
    rental_amount: int = Column(Integer)
    lease_start_date: date = Column(Date)
    lease_end_date: date = Column(Date)
    unit_area: int = Column(Integer)
    has_reception: bool = Column(Boolean)


