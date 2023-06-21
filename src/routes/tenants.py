from flask import Blueprint, render_template, request

from src.database.models.companies import Company
from src.database.models.tenants import QuotationForm
from src.main import tenant_controller, company_controller
from src.authentication import login_required
from src.database.models.users import User

tenants_route = Blueprint('tenants', __name__)


@tenants_route.get('/admin/tenants')
@login_required
async def get_tenants(user: User):
    user_data = user.dict()

    companies: list[Company] = await company_controller.get_user_companies(user_id=user.user_id)
    companies_dicts = [company.dict() for company in companies]
    context = dict(user=user_data, companies=companies_dicts)

    return render_template('tenants/get_tenant.html', **context)


@tenants_route.post('/admin/add-tenants')
@login_required
async def do_add_tenants(user: User):
    user_data = user.dict()
    context = dict(user=user_data)

    return render_template('tenants/get_tenant.html', **context)


@tenants_route.post('/admin/tenant-rentals')
@login_required
async def tenant_rentals(user: User):
    user_data = user.dict()
    context = dict(user=user_data)
    tenant_quote = QuotationForm(**request.form)
    print(tenant_quote)
    return render_template('tenants/get_tenant.html', **context)

