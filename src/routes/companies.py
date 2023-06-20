from flask import Blueprint, render_template, request, url_for, redirect, flash
from pydantic import ValidationError

from src.logger import init_logger
from src.database.models.properties import Property
from src.database.models.bank_accounts import BusinessBankAccount
from src.authentication import login_required
from src.database.models.users import User
from src.database.models.companies import Company
from src.controller.companies import CompaniesController

companies_route = Blueprint('companies', __name__)
companies_logger = init_logger('companies_logger')


@companies_route.get('/admin/companies')
@login_required
async def get_companies(user: User):
    user_data = user.dict()
    companies_controller = CompaniesController()
    companies: list[Company] = await companies_controller.get_user_companies(user_id=user.user_id)
    companies_dict = [company.dict() for company in companies if company] if isinstance(companies, list) else []

    context = dict(user=user_data,
                   companies=companies_dict)

    return render_template('companies/companies.html', **context)


@companies_route.get('/admin/company/<string:company_id>')
@login_required
async def get_company(user: User, company_id: str):
    user_data = user.dict()
    companies_controller = CompaniesController()
    company: Company = await companies_controller.get_company(company_id=company_id, user_id=user.user_id)
    properties: list[Property] = await companies_controller.get_properties(company_id=company_id)

    bank_accounts: list[BusinessBankAccount] = await companies_controller.get_bank_accounts(company_id=company_id)
    properties_dict = [prop.dict() for prop in properties if prop] if isinstance(properties, list) else []
    bank_accounts_dicts = [account.dict() for account in bank_accounts if account] if isinstance(bank_accounts,
                                                                                                 list) else []

    context = dict(user=user_data,
                   company=company.dict(),
                   properties=properties_dict,
                   bank_accounts=bank_accounts_dicts)

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
    try:
        company_data = Company(**form_data)
        companies_controller = CompaniesController()
        _company_data = await companies_controller.create_company(company=company_data, user=user)

        _message = f"Company {_company_data.company_name} Added Successfully"
        flash(message=_message, category="success")
    except ValidationError as e:
        companies_logger.error(str(e))
        flash(message="Error creating Company please fill in all required fields", category='danger')

    return redirect(url_for('companies.get_companies'))


@companies_route.post('/admin/company/add-bank-account/<string:company_id>')
@login_required
async def do_add_bank_account(user: User, company_id: str):
    try:
        bank_account_details: BusinessBankAccount = BusinessBankAccount(**request.form)
        if company_id == bank_account_details.company_id:
            flash(message='Ounch That one hurt ', category="danger")
            return redirect(url_for('home.get_home'))
        companies_controller = CompaniesController()
        _ = await companies_controller.update_bank_account(account_details=bank_account_details)

        flash(message="successfully updated company bank account details", category="success")

    except ValidationError as e:
        companies_logger.error(str(e))
        flash(message="Error creating Bank Account please fill in all the details", category="danger")

    return redirect(url_for('companies.get_company', company_id=company_id))
