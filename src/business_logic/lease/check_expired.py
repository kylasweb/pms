"""
    checks for expired lease agreements -
    create in app notices to the administrator for the company in which
    the agreement has expired

    inform the client of this situation

"""

from datetime import date, timedelta
from typing import List

from database.models.companies import Company
from database.models.properties import Property, Unit
from src.emailer import SendMail, EmailModel
from src.database.models.tenants import Tenant
from src.database.models.lease import LeaseAgreement
from src.main import tenant_controller, company_controller
from src.config import config_instance

settings = config_instance().EMAIL_SETTINGS


class LeaseAgreementNotifier:
    """
        **LeaseAgreementNotifier**

    """

    def __init__(self, _agreements: List[LeaseAgreement], notify_days_before: int = 30):
        self.notify_days_before = notify_days_before
        self.agreements = _agreements
        self._send_mail = SendMail()

    async def send_tenant_email(self, agreement: LeaseAgreement):
        company, property_, tenant = await self.get_client_data(agreement)

        message, subject = await self.create_template(company, property_, tenant)

        email_dict = {
            'from_': settings.RESEND.from_,
            'to_': tenant.email,
            'subject_': subject,
            'html': message
        }

        email_ = EmailModel(**email_dict)
        await self._send_mail.send_mail_resend(email=email_)

    @staticmethod
    async def create_template(company: Company, property_: Property, tenant: Tenant):
        subject = f"{property_.name} Lease Agreement Expiry Notification"
        message = f"""
            Hi {tenant.name},

            Your Lease Agreement between you and {company.company_name}
            for a unit in Building / Property {property_.name}
            has expired.

            If you wish to renew this lease agreement, 
            please notify your landlord immediately: {property_.landlord}
            Contact Number: {property_.maintenance_contact}

            Thank you,
            {company.company_name}
            Tel: {company.contact_number}
            Email: {company.province}
        """
        return message, subject

    @staticmethod
    async def get_client_data( agreement: LeaseAgreement):
        property_ = await company_controller.get_company_internal(property_id=agreement.property_id)
        company = await company_controller.get_company_internal(company_id=property_.company_id)
        tenant = await tenant_controller.get_tenant_by_id(tenant_id=agreement.tenant_id)
        unit_ = await company_controller.get_unit_by_unit_id_internal(unit_id=agreement.unit_id)
        return company, property_, tenant

    async def check_agreements_about_to_expire(self):
        """
        **check_agreements_about_to_expire**
            this will only return agreements which are about to expire not those
            already expired.
        :return:
        """
        today = date.today()
        expiration_threshold = today + timedelta(days=self.notify_days_before)
        return [
            agreement
            for agreement in self.agreements
            if ((agreement.end_date <= expiration_threshold) and agreement.days_left)
        ]

    async def check_expired_agreements(self):
        today = date.today()
        expired_agreements = [
            agreement
            for agreement in self.agreements
            if agreement.end_date < today
        ]
        return expired_agreements

    async def send_notifications(self, agreement: LeaseAgreement):
        await self.send_tenant_email(agreement=agreement)

    async def process_expired_agreements(self):
        """find expired lease agreements"""

        expired_agreements = await self.check_expired_agreements()
        for agreement in expired_agreements:
            await self.send_notifications(agreement=agreement)
            await self.clear_unit_for_booking(agreement)

        expiring_agreements = await self.check_agreements_about_to_expire()
        for agreement in expiring_agreements:
            await self.send_notifications(agreement=agreement)

    async def clear_unit_for_booking(self, agreement: LeaseAgreement):
        """

        :param agreement:
        :return:
        """
        pass


if __name__ == "__main__":
    # Example usage
    agreements = [
        LeaseAgreement(agreement_id="A001", client_id="C001", expiration_date=date(2023, 6, 20)),
        LeaseAgreement(agreement_id="A002", client_id="C002", expiration_date=date(2023, 6, 25)),
        LeaseAgreement(agreement_id="A003", client_id="C003", expiration_date=date(2023, 6, 18)),
    ]

    notifier = LeaseAgreementNotifier(agreements)
    notifier.process_expired_agreements()
