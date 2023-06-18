from flask import Blueprint, render_template
from src.authentication import login_required
from src.database.models.users import User

companies_route = Blueprint('companies', __name__)


@companies_route.get('/admin/companies')
@login_required
async def get_companies(user: User):
    user_data = user.dict()
    context = dict(user=user_data)
    # TODO load company data based on user data
    return render_template('companies/companies.html', **context)


@companies_route.get('/admin/create-company')
@login_required
async def create_company(user: User):
    user_data = user.dict()
    context = dict(user=user_data)
    # TODO load company data based on user data
    return render_template('companies/create_company.html', **context)
