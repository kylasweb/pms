from pydantic import BaseModel
from typing import List
from src.database.models.address import Address


class Property(BaseModel):
    property_id: str
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


class OfficeShop(BaseModel):
    property_id: str
    is_occupied: bool
    rental_amount: int
    tenant_name: str
    lease_start_date: str
    lease_end_date: str
    office_area: int
    has_reception: bool
