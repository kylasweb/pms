from src.controller import error_handler
from src.database.models.properties import Unit, Property
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
    @staticmethod
    @error_handler
    async def get_tenant_by_id(tenant_id: str) -> Tenant | None:
        """

        :param tenant_id:
        :return:
        """
        with Session() as session:
            tenant = session.query(TenantORM).filter(TenantORM.tenant_id == tenant_id).first()
            if isinstance(tenant, TenantORM):
                return Tenant(**tenant.to_dict())
            return None

    @error_handler
    async def create_quotation(self, user: User, quotation: QuotationForm) -> dict[str, Unit | Property]:
        """
        **create_quotation**

        :param user:
        :param quotation:
        :return:
        """
        self._logger.info(f"Creating Quotation with : {quotation}")

        property_listed: Property = await company_controller.get_property(user=user, property_id=quotation.property_id)
        property_units: list[Unit] = await company_controller.get_un_leased_units(
            user=user, property_id=quotation.building)
        # TODO - create a smarter recommendation algorithm for quotations
        min_rental_unit: Unit = min(property_units, key=lambda unit: unit.rental_amount)
        max_rental_unit: Unit = max(property_units, key=lambda unit: unit.rental_amount)

        quote: dict[str, Unit | Property] = {'recommended_unit': min_rental_unit,
                                             'alternate_unit': max_rental_unit,
                                             'property': property_listed
                                             }

        return quote
