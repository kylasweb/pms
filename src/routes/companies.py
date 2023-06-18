from flask import Blueprint, render_template
from src.authentication import login_required
from src.database.models.users import User
from src.view.companies import CompaniesView

companies_route = Blueprint('companies', __name__)


@companies_route.get('/admin/companies')
@login_required
async def get_companies(user: User):
    user_data = user.dict()
    companies_view = CompaniesView()
    companies = await companies_view.get_user_companies(user_id=user.user_id)
    context = dict(user=user_data, companies=[company.dict() for company in companies])
    # TODO load company data based on user data
    return render_template('companies/companies.html', **context)


@companies_route.get('/admin/company/<string:company_id>')
@login_required
async def get_company(user: User, company_id: str):
    user_data = user.dict()
    companies_view = CompaniesView()
    company = await companies_view.get_company(company_id=company_id, user_id=user.user_id)

    context = dict(user=user_data, company=company.dict())
    # TODO load company data based on user data
    return render_template('companies/company.html', **context)


@companies_route.get('/admin/create-company')
@login_required
async def create_company(user: User):
    user_data = user.dict()
    context = dict(user=user_data)
    # TODO load company data based on user data
    return render_template('companies/create_company.html', **context)
