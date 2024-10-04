"""
    checks for expired lease agreements -
    create in app notices to the administrator for the company_id in which
    the agreement has expired

    inform the client of this situation

"""

from datetime import date, timedelta, datetime
from typing import List

from src.database.models.companies import Company
from src.database.models.properties import Property, Unit
from src.database.sql import Session
from src.database.sql.companies import UserCompanyORM
from src.database.sql.notifications import NotificationORM
from src.database.sql.properties import PropertyORM
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
        company, property_, tenant, unit_ = await self.get_client_data(agreement)

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
    async def get_client_data(agreement: LeaseAgreement) -> tuple[Company, Property, Tenant, Unit]:
        property_ = await company_controller.get_company_internal(property_id=agreement.property_id)
        company = await company_controller.get_company_internal(company_id=property_.company_id)
        tenant = await tenant_controller.get_tenant_by_id(tenant_id=agreement.tenant_id)
        unit_ = await company_controller.get_unit_by_unit_id_internal(unit_id=agreement.unit_id)
        return company, property_, tenant, unit_

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
        return (
            [
                agreement
                for agreement in self.agreements
                if agreement.end_date < today
            ]
            if isinstance(self.agreements, list)
            else []
        )

    async def send_notice_to_company_admins(self, agreement: LeaseAgreement):
        """
        **send_notice_to_admin**
        Admin notices will also be visible on
        the web application as messages.

        :param agreement: LeaseAgreement object
        :return: None
        """
        # Retrieve the company_id ID from the property
        company, property_, tenant, unit_ = await self.get_client_data(agreement)

        # Retrieve the admin user ID for the company_id
        user_company_list: list[UserCompanyORM] = await company_controller.user_company_id(
            company_id=property_.company_id)

        if not user_company_list:
            # Admin user not found, handle accordingly
            return

        await self.create_notice_admin(company=company, property_=property_, tenant=tenant,
                                       user_company_list=user_company_list)

        # Return or perform any necessary operations
        return

    async def create_notice_admin(self, company, property_, tenant, user_company_list):
        """
            creates an in-app notifications which will be seen by property admins
            when they Login
        :param company:
        :param property_:
        :param tenant:
        :param user_company_list:
        :return:
        """
        with Session() as session:
            # Create a new notification
            for user in user_company_list:
                if user.user_level.casefold() == "admin":
                    message = await self.create_admin_notification_message(tenant=tenant, company=company,
                                                                           property_=property_)
                    subject = f'Lease Agreement Expiration : for Tenant {tenant.name}'
                    notification = NotificationORM(
                        user_id=user.user_id,
                        title=subject,
                        message=message,
                        category='Expiration',
                        time_read=None,
                        is_read=False,
                        time_created=datetime.now()
                    )
                    session.add(notification)

            session.commit()

    @staticmethod
    async def create_admin_notification_message(tenant: Tenant, company: Company, property_: Property):
        return f"""
            Hi Admin
            
            A Lease Agreement for {tenant.name},
            
    
            On Company {company.company_name}
            for a unit in Building / Property {property_.name}
            has expired.
    
            Consider Notifying the client if they intend to renew the agreement 
             
            Note: An Email has been sent to the client informing them of the status of their 
            lease agreement, should you wish to make a follow up here are the client details 
            
            Name: {tenant.name}
            Cell: {tenant.phone_number}
            Email: {tenant.email}
            Lease Start Date : {tenant.lease_start_date}
            Lease Ended: {tenant.lease_end_date}

            Thank you,
                Property & Rental Manager 
                https://rental-manager.ste
        """

    async def send_notifications(self, agreement: LeaseAgreement):
        await self.send_tenant_email(agreement=agreement)
        await self.send_notice_to_company_admins(agreement=agreement)

    async def process_expired_agreements(self):
        """find expired lease agreements"""

        expired_agreements = await self.check_expired_agreements()
        for agreement in expired_agreements:
            await self.send_notifications(agreement=agreement)

        expiring_agreements = await self.check_agreements_about_to_expire()
        for agreement in expiring_agreements:
            await self.send_notifications(agreement=agreement)


if __name__ == "__main__":
    # Example usage
    agreements = [
        LeaseAgreement(agreement_id="A001", client_id="C001", expiration_date=date(2023, 6, 20)),
        LeaseAgreement(agreement_id="A002", client_id="C002", expiration_date=date(2023, 6, 25)),
        LeaseAgreement(agreement_id="A003", client_id="C003", expiration_date=date(2023, 6, 18)),
    ]

    notifier = LeaseAgreementNotifier(agreements)
    notifier.process_expired_agreements()
