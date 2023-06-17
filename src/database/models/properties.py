from datetime import date
import uuid
from pydantic import BaseModel, Field
from typing import List
from src.database.models.address import Address


class Property(BaseModel):
    property_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Property ID")
    address: Address
    property_type: str
    number_of_units: int
    available_units: int
    amenities: List[str]
    landlord: str
    maintenance_contact: str
    lease_terms: str
    description: str
    built_year: int
    parking_spots: int


class Unit(BaseModel):
    property_id: str
    unit_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unit ID")
    is_occupied: bool
    rental_amount: int
    tenant_id: str
    lease_start_date: date
    lease_end_date: date
    unit_area: int
    has_reception: bool


class LeaseAgreement(BaseModel):
    """
    Represents a lease agreement.

    Attributes:
    - agreement_id (str): The ID of the lease agreement.
    - property_id (str): The ID of the property associated with the agreement.
    - tenant_id (str): The ID of the tenant associated with the agreement.
    - start_date (date): The start date of the lease.
    - end_date (date): The end date of the lease.
    - rent_amount (float): The monthly rent amount.
    - deposit_amount (float): The security deposit amount.
    - is_active (bool): Indicates if the lease agreement is currently active.
    """

    agreement_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Agreement ID")
    property_id: str
    tenant_id: str
    start_date: date
    end_date: date
    rent_amount: float
    deposit_amount: float
    is_active: bool
