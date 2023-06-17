from pydantic import BaseModel


class Address(BaseModel):
    address_id: str
    street: str
    city: str
    state: str
    postal_code: str

