import uuid

from src.database.sql.tenants import TenantORM
from src.database.models.tenants import Tenant
from src.database.sql.bank_account import BankAccountORM
from src.database.models.bank_accounts import BusinessBankAccount
from src.database.models.properties import Property, Unit, AddUnit, UpdateProperty
from src.database.sql.properties import PropertyORM, UnitORM
from src.database.sql import Session
from src.database.models.users import User
from src.database.models.companies import Company, UpdateCompany
from src.database.sql.companies import CompanyORM, UserCompanyORM
from src.controller import error_handler, UnauthorizedError


class TenantController:
    def __init__(self):
        pass

    @staticmethod
    @error_handler
    async def get_tenant_by_cell(user: User, cell: str) -> Tenant | None:
        """

        :param user:
        :param cell:
        :return:
        """
        with Session() as session:
            tenant = session.query(TenantORM).filter(TenantORM.cell == cell).first()
            if isinstance(tenant, TenantORM):
                return Tenant(**tenant.to_dict())
            return None