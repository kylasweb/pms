from src.database.sql import Session
from src.controller import error_handler
from src.database.sql.lease import LeaseAgreementORM
from src.database.models.lease import LeaseAgreement, CreateLeaseAgreement


class LeaseController:
    def __init__(self):
        pass

    @error_handler
    async def get_all_active_lease_agreements(self) -> list[LeaseAgreement]:
        with Session() as session:
            lease_agreements: list[LeaseAgreementORM] = session.query(LeaseAgreementORM).filter(
                LeaseAgreementORM.is_active == True).all()
            return [LeaseAgreement(**lease.dict()) for lease in lease_agreements]

    @error_handler
    async def create_lease_agreement(self, lease: CreateLeaseAgreement) -> LeaseAgreement:
        """

        :param lease:
        :return:
        """
        with Session() as session:
            lease_orm: LeaseAgreementORM = LeaseAgreementORM(**lease.dict())
            session.add(lease_orm)
            session.commit()
            return LeaseAgreement(**lease.dict())
