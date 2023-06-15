from flask import Blueprint, render_template

companies_route = Blueprint('companies', __name__)


@companies_route.get('/admin/companies')
async def get_companies():
    return render_template('companies/companies.html')

@companies_route.get('/admin/create-company')
async def create_company():
    return render_template('companies/create_company.html')