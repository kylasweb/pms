from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from datetime import date

from sqlalchemy.orm import relationship

from src.database.constants import ID_LEN, NAME_LEN
from src.database.sql import Base


class InvoiceORM(Base):
    __tablename__ = 'invoices'
    invoice_number: str = Column(String(ID_LEN), primary_key=True)
    tenant_id: str = Column(String, ForeignKey('tenants.tenant_id'))
    month: str = Column(String(NAME_LEN))
    amount: int = Column(Integer)
    due_date: date = Column(Date)
    items = Column(Text)
