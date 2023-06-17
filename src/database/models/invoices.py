from pydantic import BaseModel
from datetime import date
from src.database.models.tenants import Tenant


class Invoice(BaseModel):
    invoice_number: str
    month: str
    amount: float
    due_date: date
    tenant: Tenant
    items: list[str]

