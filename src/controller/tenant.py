from src.controller import error_handler
from src.database.models.properties import Unit
from src.database.models.tenants import Tenant, QuotationForm
from src.database.models.users import User
from src.database.sql import Session
from src.database.sql.tenants import TenantORM
from src.logger import init_logger
from src.main import company_controller


class TenantController:
    def __init__(self):
        self._logger = init_logger(self.__class__.__name__)

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

    @error_handler
    async def create_quotation(self, user: User, quotation: QuotationForm):
        """

        :param user:
        :param quotation:
        :return:
        """

        self._logger.info(f"Creating Quotation with : {quotation}")

        property_units: list[Unit] = await company_controller.get_un_leased_units(
            user=user, property_id=quotation.building)

        min_rental_unit: Unit = min([unit for unit in property_units], key=lambda unit: unit.rental_amount)
        max_rental_unit: Unit = max([unit for unit in property_units], key=lambda unit: unit.rental_amount)

        return await self.do_quote(min_rental_unit, max_rental_unit)

    @error_handler
    async def do_quote(self, min_rental_unit: Unit, max_rental_unit: Unit):
        pass
