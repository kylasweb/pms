from src.database.sql import Session
from src.database.models.companies import Company
from src.database.sql.companies import CompanyORM, UserCompanyORM

import uuid

companies_temp_data = [
    {
        "company_id": str(uuid.uuid4()),
        "company_name": "OpenAI",
        "description": "OpenAI is an artificial intelligence research laboratory consisting of the for-profit corporation OpenAI LP and its parent company, the non-profit OpenAI Inc.",
        "address_line_1": "3180 18th Street",
        "address_line_2": "San Francisco, CA",
        "city": "San Francisco",
        "postal_code": "94110",
        "province": "California",
        "country": "United States",
        "contact_number": "+1 (415) 529-5202",
        "website": "www.openai.com"
    },
    {
        "company_id": str(uuid.uuid4()),
        "company_name": "Tesla",
        "description": "Tesla, Inc. is an American electric vehicle and clean energy company. It designs, manufactures, and sells electric cars, solar energy products, energy storage solutions, and more.",
        "address_line_1": "3500 Deer Creek Road",
        "address_line_2": "Palo Alto, CA",
        "city": "Palo Alto",
        "postal_code": "94304",
        "province": "California",
        "country": "United States",
        "contact_number": "+1 (650) 681-5000",
        "website": "www.tesla.com"
    },
    {
        "company_id": str(uuid.uuid4()),
        "company_name": "Google",
        "description": "Google is a multinational technology company specializing in Internet-related services and products. It provides search engine services, online advertising technologies, cloud computing, software, and more.",
        "address_line_1": "1600 Amphitheatre Parkway",
        "address_line_2": "",
        "city": "Mountain View",
        "postal_code": "94043",
        "province": "California",
        "country": "United States",
        "contact_number": "+1 (650) 253-0000",
        "website": "www.google.com"
    },
    {
        "company_id": str(uuid.uuid4()),
        "company_name": "Microsoft",
        "description": "Microsoft Corporation is an American multinational technology company. It develops, manufactures, licenses, supports, and sells computer software, consumer electronics, personal computers, and more.",
        "address_line_1": "One Microsoft Way",
        "address_line_2": "",
        "city": "Redmond",
        "postal_code": "98052",
        "province": "Washington",
        "country": "United States",
        "contact_number": "+1 (425) 882-8080",
        "website": "www.microsoft.com"
    },
    {
        "company_id": str(uuid.uuid4()),
        "company_name": "Amazon",
        "description": "Amazon.com, Inc. is an American multinational technology company. It focuses on e-commerce, cloud computing, digital streaming, and artificial intelligence.",
        "address_line_1": "410 Terry Avenue North",
        "address_line_2": "",
        "city": "Seattle",
        "postal_code": "98109",
        "province": "Washington",
        "country": "United States",
        "contact_number": "+1 (206) 266-1000",
        "website": "www.amazon.com"
    }
]


class CompaniesView:
    def __init__(self):
        pass

    @staticmethod
    async def get_user_companies(user_id: str) -> list[Company]:
        """
            returns a list of user companies
        :param user_id:
        :return:
        """
        with Session() as session:
            user_company_list = session.query(UserCompanyORM).filter(UserCompanyORM.user_id == user_id).all()
            _companies = []
            for user_company in user_company_list:
                _companies.append(session.query(CompanyORM).filter(CompanyORM.company_id == user_company.company_id).first())
            response = []
            if _companies:
                for _company in _companies:
                    response.append(Company.from_orm(_company))
            else:
                for _company in companies_temp_data:
                    response.append(Company(**_company))
            return response

    @staticmethod
    async def get_company(company_id: str, user_id: str) -> Company:
        """

        :param company_id:
        :param user_id:
        :return:
        """
        with Session() as session:
            is_company_member = session.query(UserCompanyORM).filter(UserCompanyORM.user_id == user_id, UserCompanyORM.company_id).first()
            if not is_company_member:
                return None
            company_orm = session.query(CompanyORM).filter(CompanyORM.company_id == company_id).first()
            return Company.from_orm(company_orm)
