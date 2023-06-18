from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, inspect
from datetime import date
from src.database.constants import ID_LEN, NAME_LEN
from src.database.sql import Base, engine


class PropertyORM(Base):
    __tablename__ = 'properties'

    property_id = Column(String(ID_LEN), primary_key=True)
    company_id = Column(String(ID_LEN), index=True)
    name: str = Column(String(NAME_LEN))
    property_type = Column(String(NAME_LEN))
    number_of_units = Column(Integer)
    available_units: int = Column(Integer)
    amenities: str = Column(String(255))
    landlord: str = Column(String(64))
    maintenance_contact: str = Column(String(64))
    lease_terms: str = Column(Text)
    description: str = Column(Text)
    built_year: int = Column(Integer)
    parking_spots: int = Column(Integer)

    def to_dict(self) -> dict[str, str]:
        return {
            'property_id': self.property_id,
            'company_id': self.company_id,
            'name': self.name,
            'property_type': self.property_type,
            'number_of_units': self.number_of_units,
            'available_units': self.available_units,
            'amenities': self.amenities,
            'landlord': self.landlord,
            'maintenance_contact': self.maintenance_contact,
            'lease_terms': self.lease_terms,
            'description': self.description,
            'built_year': self.built_year,
            'parking_spots': self.parking_spots
        }

    @classmethod
    def create_if_not_table(cls):
        if not inspect(engine).has_table(cls.__tablename__):
            Base.metadata.create_all(bind=engine)


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

    @classmethod
    def create_if_not_table(cls):
        if not inspect(engine).has_table(cls.__tablename__):
            Base.metadata.create_all(bind=engine)
