"""
    checks for expired lease agreements -
    create in app notices to the administrator for the company in which
    the agreement has expired

    inform the client of this situation

"""

from datetime import date, timedelta
from typing import List

from database.models.lease import LeaseAgreement


class LeaseAgreementNotifier:
    """
        **LeaseAgreementNotifier**

    """

    def __init__(self, _agreements: List[LeaseAgreement], notify_days_before: int = 30):
        self.notify_days_before = notify_days_before
        self.agreements = _agreements

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
        print(
            f"Notifying administrator: Lease agreement {agreement.agreement_id} with client {agreement.client_id} has expired.")
        print(f"Notifying client: Your lease agreement {agreement.agreement_id} has expired.")

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
