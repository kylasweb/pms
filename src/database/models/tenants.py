import uuid
from datetime import date
from pydantic import BaseModel, Field


class Tenant(BaseModel):
    tenant_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="The unique ID of tenant.")
    name: str
    email: str
    phone_number: str
    address_id: str
    lease_start_date: date
    lease_end_date: date
