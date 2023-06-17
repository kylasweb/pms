from pydantic import BaseModel


class Tenant(BaseModel):
    tenant_id: str
    name: str
    email: str
    phone_number: str
    address: str
    lease_start_date: str
    lease_end_date: str
