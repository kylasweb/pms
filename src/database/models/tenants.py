from datetime import date
from pydantic import BaseModel


class Tenant(BaseModel):
    tenant_id: str
    name: str
    email: str
    phone_number: str
    address_id: str
    lease_start_date: date
    lease_end_date: date
