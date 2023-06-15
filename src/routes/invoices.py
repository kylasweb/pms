from flask import Blueprint, render_template

invoices_route = Blueprint('invoices', __name__)


@invoices_route.get('/admin/invoices')
async def get_invoices():
    return render_template('invoices/invoices.html')

