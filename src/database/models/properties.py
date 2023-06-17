from datetime import date
import uuid
from pydantic import BaseModel, Field
from typing import List
from src.database.models.address import Address



class Property(BaseModel):
    """
    Represents a property.

    Attributes:
    - property_id (str): The ID of the property.
    - address (Address): The address of the property.
    - property_type (str): The type of the property.
    - number_of_units (int): The total number of units in the property.
    - available_units (int): The number of units currently available.
    - amenities (List[str]): The list of amenities available in the property.
    - landlord (str): The name of the landlord.
    - maintenance_contact (str): The contact information for property maintenance.
    - lease_terms (str): The terms and conditions of the lease.
    - description (str): A description of the property.
    - built_year (int): The year the property was built.
    - parking_spots (int): The number of parking spots available in the property.
    """

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
    """
    Represents a unit in a property.

    Attributes:
    - property_id (str): The ID of the property the unit belongs to.
    - unit_id (str): The ID of the unit.
    - is_occupied (bool): Indicates if the unit is currently occupied.
    - rental_amount (int): The rental amount for the unit.
    - tenant_id (str): The ID of the tenant occupying the unit.
    - lease_start_date (date): The start date of the lease for the unit.
    - lease_end_date (date): The end date of the lease for the unit.
    - unit_area (int): The area of the unit in square feet.
    - has_reception (bool): Indicates if the unit has a reception area.
    """

    property_id: str
    unit_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unit ID")
    is_occupied: bool
    rental_amount: int
    tenant_id: str
    lease_start_date: date
    lease_end_date: date
    unit_area: int
    has_reception: bool
