from flask import Blueprint, render_template, flash, redirect, url_for, request

cron_route = Blueprint('cron', __name__)


@cron_route.get('/cron/lease')
async def check_lease_expiry():
    lease_agreements =
    await lease_agreement_notifier.process_expired_agreements()


