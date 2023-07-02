import uuid
from datetime import date
from pydantic import BaseModel, Field, validator


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

    tenant_id: str
    address_id: str | None
    name: str
    id_number: str
    company_id: str | None
    email: str
    cell: str
    is_renting: bool
    lease_start_date: date | None
    lease_end_date: date | None

    @classmethod
    @validator("lease_start_date", pre=True)
    def validate_lease_start_date(cls, value):
        return None if not isinstance(value, date) else value

    @classmethod
    @validator("lease_end_date", pre=True)
    def validate_lease_end_date(cls, value):
        return None if not isinstance(value, date) else value


class CreateTenant(BaseModel):
    tenant_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="The unique ID of the tenant.")
    address_id: str | None
    name: str
    company_id: str | None
    id_number: str
    email: str
    cell: str
    is_renting: bool = Field(default=False)
    lease_start_date: date | None
    lease_end_date: date | None


class QuotationForm(BaseModel):
    tenant_name: str
    tenant_company: str
    tenant_cell: str
    tenant_email: str
    company: str | None
    building: str | None
    booking_type: str | None
    lease_start_date: date | None = None
    lease_end_date: date | None = None

    @property
    def property_id(self) -> str:
        return self.company
