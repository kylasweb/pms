import uuid

from pydantic import BaseModel, Field


class Company(BaseModel):
    """
    Represents the details of a company.

    Attributes:
    - company_name (str): The name of the company.
    - address (str): The address of the company.
    - city (str): The city where the company is located.
    - state (str): The state where the company is located.
    - country (str): The country where the company is located.
    - postal_code (str): The postal code of the company's address.
    - contact_number (str): The contact number of the company.
    - website (str): The website URL of the company.
    """

    company_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_name: str | None
    description: str | None

    address_line_1: str | None
    address_line_2: str | None
    city: str | None
    postal_code: str | None
    province: str | None
    country: str | None
    contact_number: str | None
    website: str | None

    class Config:
        from_orm = True

class UpdateCompany(BaseModel):
    company_id: str
    company_name: str
    description: str

    address_line_1: str | None
    address_line_2: str | None
    city: str
    postal_code: str
    province: str
    country: str
    contact_number: str
    website: str
