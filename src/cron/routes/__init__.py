from flask import Blueprint, render_template, flash, redirect, url_for, request

from src.database.models.lease import LeaseAgreement
from src.main import lease_agreement_controller
from src.business_logic.lease.check_expired import LeaseAgreementNotifier

cron_route = Blueprint('cron', __name__)


@cron_route.get('/cron/lease')
async def check_lease_expiry():
    lease_agreements: list[LeaseAgreement] = await lease_agreement_controller.get_all_active_lease_agreements()
    lease_agreement_processor = LeaseAgreementNotifier(_agreements=lease_agreements)
    await lease_agreement_processor.process_expired_agreements()
    return dict(status="Success")



