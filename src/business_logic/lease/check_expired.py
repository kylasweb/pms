"""
    checks for expired lease agreements -
    create in app notices to the administrator for the company in which
    the agreement has expired

    inform the client of this situation

"""

from datetime import date
from typing import List
from pydantic import BaseModel


class LeaseAgreement(BaseModel):
    agreement_id: str
    client_id: str
    expiration_date: date


class LeaseAgreementNotifier:
    def __init__(self, agreements: List[LeaseAgreement]):
        self.agreements = agreements

    def check_expired_agreements(self):
        today = date.today()
        expired_agreements = [
            agreement
            for agreement in self.agreements
            if agreement.expiration_date < today
        ]
        return expired_agreements

    def notify_administrator(self, agreement: LeaseAgreement):
        print(
            f"Notifying administrator: Lease agreement {agreement.agreement_id} with client {agreement.client_id} has expired.")

    def notify_client(self, agreement: LeaseAgreement):
        print(f"Notifying client: Your lease agreement {agreement.agreement_id} has expired.")

    def process_expired_agreements(self):
        expired_agreements = self.check_expired_agreements()
        for agreement in expired_agreements:
            self.notify_administrator(agreement)
            self.notify_client(agreement)


# Example usage
agreements = [
    LeaseAgreement(agreement_id="A001", client_id="C001", expiration_date=date(2023, 6, 20)),
    LeaseAgreement(agreement_id="A002", client_id="C002", expiration_date=date(2023, 6, 25)),
    LeaseAgreement(agreement_id="A003", client_id="C003", expiration_date=date(2023, 6, 18)),
]

notifier = LeaseAgreementNotifier(agreements)
notifier.process_expired_agreements()
