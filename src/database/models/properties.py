from pydantic import BaseModel
from src.database.models.address import Address

class Property(BaseModel):
    address: Address
    property_type: str
    number_of_units: int
    available_units: int
    amenities: list[str]
    landlord: str
    maintenance_contact: str
    lease_terms: str
