from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, inspect
from datetime import date
from src.database.constants import ID_LEN, NAME_LEN
from src.database.sql import Base, engine


class TenantORM(Base):
    __tablename__ = 'tenants'

    tenant_id: str = Column(String(ID_LEN), primary_key=True)
    address_id: str = Column(String(ID_LEN), ForeignKey('addresses.address_id'))
    name: str = Column(String(NAME_LEN))
    company: str = Column(String(NAME_LEN))
    email: str = Column(String(256))
    cell: str = Column(String(13))
    lease_start_date: date = Column(Date)
    lease_end_date: date = Column(Date)

    @classmethod
    def create_if_not_table(cls):
        if not inspect(engine).has_table(cls.__tablename__):
            Base.metadata.create_all(bind=engine)

    def to_dict(self):
        """
        Convert the TenantORM object to a dictionary.

        :return: A dictionary representation of the object.
        """
        return {
            'tenant_id': self.tenant_id,
            'address_id': self.address_id,
            'name': self.name,
            'company': self.company,
            'email': self.email,
            'cell': self.cell,
            'lease_start_date': str(self.lease_start_date),
            'lease_end_date': str(self.lease_end_date)
        }
