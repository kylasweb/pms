from flask import Blueprint, render_template, request, url_for, redirect, flash
from src.authentication import login_required
from src.database.models.users import User
from src.database.models.companies import Company
from src.controller.companies import CompaniesController


companies_route = Blueprint('companies', __name__)


@companies_route.get('/admin/companies')
@login_required
async def get_companies(user: User):
    user_data = user.dict()
    companies_controller = CompaniesController()
    companies = await companies_controller.get_user_companies(user_id=user.user_id)
    context = dict(user=user_data,
                   companies=[company.dict() for company in companies])

    return render_template('companies/companies.html', **context)


@companies_route.get('/admin/company/<string:company_id>')
@login_required
async def get_company(user: User, company_id: str):
    user_data = user.dict()
    companies_controller = CompaniesController()
    company = await companies_controller.get_company(company_id=company_id, user_id=user.user_id)
    properties = await companies_controller.get_properties(company_id=company_id)
    context = dict(user=user_data,
                   company=company.dict(),
                   properties=[prop.dict() for prop in properties])

    return render_template('companies/company.html', **context)


@companies_route.get('/admin/create-company')
@login_required
async def get_create_company(user: User):
    user_data = user.dict()
    context = dict(user=user_data)

    return render_template('companies/create_company.html', **context)


@companies_route.post('/admin/create-company')
@login_required
async def do_create_company(user: User):

    form_data = request.form
    company_data = Company(**form_data)
    companies_controller = CompaniesController()
    _company_data = await companies_controller.create_company(company=company_data, user=user)

    _message = f"Company {_company_data.company_name} Added Successfully"
    flash(message=_message, category="success")
    return redirect(url_for('companies.get_companies'))
