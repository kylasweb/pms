from flask import Blueprint, render_template
from src.authentication import login_required
from src.database.models.users import User

invoices_route = Blueprint('invoices', __name__)


@invoices_route.get('/admin/invoices')
@login_required
async def get_invoices(user: User):
    return render_template('invoices/invoices.html')

