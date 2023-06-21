import uuid
from datetime import date
from pydantic import BaseModel, Field


class Tenant(BaseModel):
    """
    Represents a tenant.

    Attributes:
    - tenant_id (str): The unique ID of the tenant.
    - name (str): The name of the tenant.
    - email (str): The email address of the tenant.
    - phone_number (str): The phone number of the tenant.
    - address_id (str): The ID of the address associated with the tenant.
    - lease_start_date (date): The start date of the lease.
    - lease_end_date (date): The end date of the lease.
    """

    tenant_id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                           description="The unique ID of the tenant.")
    name: str
    company: str
    email: str
    phone_number: str
    address_id: str
    lease_start_date: date
    lease_end_date: date
