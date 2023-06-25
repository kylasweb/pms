from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for

from src.database.models.properties import Property
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
    companies_dicts = [company.dict() for company in companies if company] if isinstance(companies, list) else []
    context = dict(user=user_data, companies=companies_dicts)

    return render_template('tenants/get_tenant.html', **context)


@tenants_route.get('/admin/tenant/buildings/<string:company_id>')
@login_required
async def get_buildings(user: User, company_id: str):

    # Query the database or perform any necessary logic to fetch the buildings based on the company_id ID

    buildings: list[Property] = await company_controller.get_properties(user=user, company_id=company_id)

    buildings_dicts = [building.dict() for building in buildings if building] if isinstance(buildings, list) else []
    # Return the buildings as JSON response
    return jsonify(buildings_dicts)


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
    tenant_quote: QuotationForm = QuotationForm(**request.form)
    quotation = await tenant_controller.create_quotation(user=user, quotation=tenant_quote)

    message = """Quote Created and Notification will be sent, via email or cell. 
    
    Lease Agreements and a Quotation will be sent via email &
    Remember you can Reprint Both the Quotation & Lease Agreement from the Tenant Details Section
    """

    flash(message=message, category="success")
    return redirect(url_for('tenants.get_tenants'))
