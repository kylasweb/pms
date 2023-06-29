"""

    Business Logic to create invoices and statements for
    tenants

"""
import asyncio
from datetime import datetime, date, timedelta

from database.models.invoices import Invoice
from src.database.sql.companies import UserCompanyORM
from src.database.sql import Session
from src.database.sql.invoices import InvoiceORM
from src.database.models.profile import Profile
from src.database.models.properties import Property
from src.database.models.companies import Company
from src.database.models.tenants import Tenant
from src.database.models.lease import LeaseAgreement
from src.main import lease_agreement_controller
from src.main import tenant_controller
from src.main import company_controller


class StatementsAndInvoicing:
    """
    **StatementsAndInvoicing**
        will create statements and invoices for each client
        who presently has a lease agreement
        Steps
        1. Notices for this steps must be created
        2.
    """

    def __init__(self):
        pass

    @staticmethod
    async def get_profile(uuid: str) -> Profile:
        """

        :param uuid:
        :return:
        """
        return Profile()

    @staticmethod
    async def monthly_lease_agreements() -> dict[str, dict[str, LeaseAgreement | Tenant | Company | Property]]:
        """
            **monthly_lease_agreements**
        :return:
        """
        monthly_lease_agreements: list[
            LeaseAgreement] = await lease_agreement_controller.get_agreements_by_payment_terms()
        _response_data = {}
        for agreement in monthly_lease_agreements:
            tenant: Tenant = await tenant_controller.get_tenant_by_id(tenant_id=agreement.tenant_id)
            company: Company = await company_controller.get_company_internal(company_id=tenant.company_id)
            property_: Property = await company_controller.get_property_by_id_internal(
                property_id=agreement.property_id)
            _data = dict(agreement=agreement, tenant=tenant, company=company, property=property_)
            _response_data[agreement.agreement_id] = _data
        return _response_data

    @staticmethod
    async def calculate_due_date(date_issued: date) -> date:
        if date_issued.day >= 7:
            if date_issued.month == 12:
                due_date = date(date_issued.year + 1, 1, 7)
            else:
                due_date = date(date_issued.year, date_issued.month + 1, 7)
        else:
            due_date = date(date_issued.year, date_issued.month, 7)

        return due_date

    @staticmethod
    async def create_invoiced_items(items: list[dict[str, str | int]]):
        """

        :param items:
        :return:
        """
        _response = []
        for item in items:
            _response.append(item.get('item_number'))
        return _response

    async def create_invoice(self,
                             lease_data: dict[str, LeaseAgreement | Tenant | Company | Property],
                             invoiced_items: list[dict[str, str | int]]):
        """

        :param invoiced_items:
        :param lease_data:
        :return:
        """
        property_: Property = lease_data.get('property')
        company: Company = lease_data.get('company')
        tenant: Tenant = lease_data.get('tenant')
        user_company: UserCompanyORM = await company_controller.internal_company_id_to_user_id(
            company_id=company.company_id)
        profile: Profile = await self.get_profile(uuid=user_company.user_id)
        service_name: str = f"{property_.name} Monthly Rental"
        description: str = f"{company.company_name} Monthly Rental Invoice for Property : {property_.name}"
        _date_issued = datetime.now().date()
        _due_date = await self.calculate_due_date(date_issued=_date_issued)
        _invoiced_items: list[str] = await self.create_invoiced_items(items=invoiced_items)
        _invoice_data = dict(service_name=service_name, description=description, currency=profile.currency,
                             customer=dict(tenant_id=tenant.tenant_id, name=tenant.name, email=tenant.email,
                                           cell=tenant.cell),
                             date_issued=_date_issued, due_date=_due_date, invoiced_items=_invoiced_items)

        with Session() as session:
            _invoice_orm: InvoiceORM = InvoiceORM(**_invoice_data)
            session.add(_invoice_orm)
            session.commit()

    async def load_invoices(self) -> list[Invoice]:
        """

        :return:
        """
        pass

    async def send_email(self, invoice: Invoice):
        pass

    async def send_invoices(self):
        """

        :return:
        """
        invoices_list: list[Invoice] = await self.load_invoices()
        for invoice in invoices_list:
            await self.send_email(invoice=invoice)
            await asyncio.sleep(360)

    async def run(self):
        lease_agreements = await self.monthly_lease_agreements()


