from datetime import date
from sqlalchemy import Column, Date, Float, Boolean, String, Integer, Text, inspect
from sqlalchemy.ext.declarative import declarative_base
from src.database.constants import ID_LEN, NAME_LEN
from src.database.sql import Base, engine


class LeaseAgreementORM(Base):
    __tablename__ = 'lease_agreement'
    agreement_id: str = Column(String(ID_LEN), primary_key=True, unique=True)
    property_id: str = Column(String(ID_LEN))
    tenant_id: str = Column(String(ID_LEN))
    start_date: date = Column(Date)
    end_date: date = Column(Date)
    rent_amount: int = Column(Integer)
    deposit_amount: int = Column(Integer)
    is_active: bool = Column(Boolean)

    @classmethod
    def create_if_not_table(cls):
        if not inspect(engine).has_table(cls.__tablename__):
            Base.metadata.create_all(bind=engine)


class LeaseAgreementTemplate(Base):
    __tablename__ = 'lease_agreement_template'

    template_id: str = Column(String(ID_LEN), primary_key=True, unique=True)
    property_id: str = Column(String(ID_LEN))
    template_name: str = Column(String(NAME_LEN))
    template_text: str = Column(Text)
    is_default: bool = Column(Boolean)

    @classmethod
    def create_if_not_table(cls):
        if not inspect(engine).has_table(cls.__tablename__):
            Base.metadata.create_all(bind=engine)

