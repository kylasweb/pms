import uuid

from src.database.sql.bank_account import BankAccountORM
from src.database.models.bank_accounts import BusinessBankAccount
from src.database.models.properties import Property, Unit, AddUnit, UpdateProperty
from src.database.sql.properties import PropertyORM, UnitORM
from src.database.sql import Session
from src.database.models.users import User
from src.database.models.companies import Company
from src.database.sql.companies import CompanyORM, UserCompanyORM
from src.controller import error_handler, UnauthorizedError

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


class CompaniesController:
    def __init__(self):
        pass

    @error_handler
    async def is_company_member(self, user_id: str, company_id: str, session):
        result: UserCompanyORM = session.query(UserCompanyORM).filter(
            UserCompanyORM.user_id == user_id, UserCompanyORM.company_id == company_id).first()
        return isinstance(result, UserCompanyORM) and (result.company_id == company_id) and (result.user_id == user_id)


    @staticmethod
    @error_handler
    async def get_user_companies(user_id: str) -> list[Company]:
        with Session() as session:
            user_company_list = session.query(UserCompanyORM).filter(UserCompanyORM.user_id == user_id).all()

            response = []
            for user_company in user_company_list:
                if isinstance(user_company, UserCompanyORM):
                    company_orm = session.query(CompanyORM).filter(
                        CompanyORM.company_id == user_company.company_id).first()
                    if isinstance(company_orm, CompanyORM):
                        response.append(Company(**company_orm.to_dict()))

            return response

    @error_handler
    async def get_company(self, company_id: str, user_id: str) -> Company | None:
        with Session() as session:
            _is_company_member: bool = await self.is_company_member(company_id=company_id,
                                                                    user_id=user_id,
                                                                    session=session)
            if not _is_company_member:
                raise UnauthorizedError('You are not authorized to access this company')

            company_orm = session.query(CompanyORM).filter(CompanyORM.company_id == company_id).first()
            return Company(**company_orm.to_dict()) if company_orm else None

    @staticmethod
    @error_handler
    async def create_company(company: Company, user: User) -> Company:
        # Perform necessary operations to create the company
        # For example, you can save the company data in a database
        # and associate it with the user
        with Session() as session:
            # TODO Check if payment is already made
            company_orm: CompanyORM = CompanyORM(**company.dict())
            response = Company(**company_orm.to_dict())
            user_company_data = dict(id=str(uuid.uuid4()), company_id=company_orm.company_id, user_id=user.user_id)
            session.add(company_orm)
            session.add(UserCompanyORM(**user_company_data))
            session.commit()

            return response

    @error_handler
    async def update_bank_account(self, user: User, account_details: BusinessBankAccount) -> BusinessBankAccount | None:
        """

        :return:
        """
        with Session() as session:
            user_id = user.user_id
            company_id = account_details.company_id
            is_company_member: bool = await self.is_company_member(user_id=user_id, company_id=company_id,
                                                                   session=session)
            if not is_company_member:
                raise UnauthorizedError(description="Not Authorized to Update Bank Account")

            bank_account_orm: BankAccountORM = BankAccountORM(**account_details.dict())
            session.add(bank_account_orm)
            session.commit()
            return account_details

    @error_handler
    async def add_property(self, user: User, _property: Property) -> Property | None:
        """

        :param user:
        :param _property:
        :return:
        """
        with Session() as session:
            user_id = user.user_id
            company_id = _property.company_id
            is_company_member: bool = await self.is_company_member(user_id=user_id, company_id=company_id,
                                                                   session=session)
            if not is_company_member:
                raise UnauthorizedError(description="Not Authorized to Add Properties to this Company")

            property_orm: PropertyORM = PropertyORM(**_property.dict())
            session.add(property_orm)
            session.commit()
            return _property

    @error_handler
    async def update_property(self, user: User, property_details: UpdateProperty) -> Property | None:
        with Session() as session:
            user_id = user.user_id
            company_id = property_details.company_id
            is_company_member: bool = await self.is_company_member(user_id=user_id,
                                                                   company_id=company_id,
                                                                   session=session)
            if not is_company_member:
                raise UnauthorizedError(description="Not Authorized to update this Property")

            original_property_orm: PropertyORM = session.query(PropertyORM).filter(
                PropertyORM.property_id == property_details.property_id).first()

            # Create a dictionary of field names and values from the property_details object
            field_updates = {field: getattr(property_details, field) for field in property_details.__fields__}

            # Update the relevant fields in original_property_orm
            for field, value in field_updates.items():
                if value:
                    setattr(original_property_orm, field, value)

            # Commit the changes to the database

            session.commit()
            return Property(**original_property_orm.to_dict())

    @error_handler
    async def get_properties(self, user: User, company_id: str) -> list[Property]:
        """

        :param user:
        :param company_id:
        :return:
        """
        with Session() as session:
            user_id = user.user_id
            is_company_member: bool = await self.is_company_member(user_id=user_id,
                                                                   company_id=company_id,
                                                                   session=session)
            if not is_company_member:
                raise UnauthorizedError(description="Not Authorized to access Properties in this Company")

            properties: list[PropertyORM] = session.query(PropertyORM).filter(
                PropertyORM.company_id == company_id).all()
            return [Property(**_prop.to_dict()) for _prop in properties]

    @error_handler
    async def get_bank_accounts(self, user: User, company_id: str) -> list[BusinessBankAccount]:
        """

        :param user:
        :param company_id:
        :return:
        """
        with Session() as session:
            user_id = user.user_id
            is_company_member: bool = await self.is_company_member(user_id=user_id,
                                                                   company_id=company_id,
                                                                   session=session)
            if not is_company_member:
                raise UnauthorizedError(description="Not Authorized to access that Bank Account")

            bank_accounts: list[BankAccountORM] = session.query(BankAccountORM).filter(
                BankAccountORM.company_id == company_id).all()

            return [BusinessBankAccount(**account.to_dict()) for account in bank_accounts]

    @error_handler
    async def get_property(self, user: User, property_id: str) -> Property:
        """

        :param user:
        :param property_id:
        :return:
        """
        with Session() as session:
            _property: PropertyORM = session.query(PropertyORM).filter(
                PropertyORM.property_id == property_id).first()

            user_id = user.user_id
            is_company_member: bool = await self.is_company_member(user_id=user_id,
                                                                   company_id=_property.company_id,
                                                                   session=session)
            if not is_company_member:
                raise UnauthorizedError(description="Not Authorized to access the Property")

            return Property(**_property.to_dict())

    @error_handler
    async def get_property_units(self, user: User, property_id: str) -> list[Unit]:
        """

        :return: False
        """
        with Session() as session:
            user_id = user.user_id

            _property: PropertyORM = session.query(PropertyORM).filter(
                PropertyORM.property_id == property_id).first()

            is_company_member: bool = await self.is_company_member(user_id=user_id,
                                                                   company_id=_property.company_id,
                                                                   session=session)
            if not is_company_member:
                raise UnauthorizedError(description="Not Authorized to access the Property")

            property_units: list[UnitORM] = session.query(UnitORM).filter(UnitORM.property_id == property_id).all()
            return [Unit(**prop.to_dict()) for prop in property_units]

    @error_handler
    async def add_unit(self, user: User, unit_data: AddUnit, property_id: str) -> AddUnit:
        """

        :param user:
        :param property_id:
        :param unit_data:
        :return:
        """
        with Session() as session:
            user_id = user.user_id

            _property: PropertyORM = session.query(PropertyORM).filter(
                PropertyORM.property_id == property_id).first()

            is_company_member: bool = await self.is_company_member(user_id=user_id,
                                                                   company_id=_property.company_id,
                                                                   session=session)
            if not is_company_member:
                raise UnauthorizedError(description="Not Authorized to access the Property")

            unit: UnitORM = UnitORM(**unit_data.dict())
            session.add(unit)
            session.commit()
            return unit_data
