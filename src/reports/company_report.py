from pydantic import BaseModel, Field, validator

from src.database.models.companies import Company


class CompanyPrintParser(BaseModel):
    company_name: str
    description: str
    address: str
    address_line_1: str
    address_line_2: str
    city: str
    postal_code: str
    province: str
    country: str
    contact_number: str
    website: str

    def to_dict(self):
        return {
            "Name": self.company_name,
            "Description": self.description,
            "Address": self.address,
            "Contact Number": self.contact_number,
            "Website": self.website}


def map_company_to_parser(company: Company) -> CompanyPrintParser:
    address_parts = [
        part
        for part in [
            company.city,
            company.province,
            company.country,
            company.postal_code,
        ]
        if part
    ]
    address = "\n".join(address_parts)

    return CompanyPrintParser(
        company_name=company.company_name or "",
        description=company.description or "",
        address=address,
        address_line_1=company.address_line_1 or "",
        address_line_2=company.address_line_2 or "",
        city=company.city or "",
        postal_code=company.postal_code or "",
        province=company.province or "",
        country=company.country or "",
        contact_number=company.contact_number or "",
        website=company.website or "",
    )
