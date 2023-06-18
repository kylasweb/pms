from pydantic import BaseModel


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

    company_id: str
    company_name: str
    description: str

    address_line_1: str
    address_line_2: str
    city: str
    postal_code: str
    province: str
    country: str
    contact_number: str
    website: str

    class Config:
        from_orm = True
