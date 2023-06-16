from pydantic import BaseModel


class Property(BaseModel):
    address: str
    property_type: str
    number_of_units: int
