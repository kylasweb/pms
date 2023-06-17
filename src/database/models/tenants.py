from pydantic import BaseModel


class Tenant(BaseModel):
    name: str
    tenant_id: str
    email: str
    phone_number: str
    address: str
    lease_start_date: str
    lease_end_date: str
