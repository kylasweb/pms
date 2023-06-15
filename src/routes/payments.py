from flask import Blueprint, render_template

payments_route = Blueprint('payments', __name__)


@payments_route.get('/admin/payments')
async def get_payments():
    return render_template('payments/payments.html')


