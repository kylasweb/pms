import logging

from flask import Blueprint, render_template, request, url_for, redirect, flash, send_file
from pydantic import ValidationError

from src.authentication import login_required
from src.controller.companies import CompaniesController
from src.database.models.bank_accounts import BusinessBankAccount
from src.database.models.companies import Company, UpdateCompany
from src.database.models.notifications import NotificationsModel
from src.database.models.properties import Property
from src.database.models.users import User
from src.logger import init_logger
from src.main import notifications_controller
from src.reports import create_report
from src.reports.bank_account_report import BankAccountPrintParser
from src.reports.company_report import map_company_to_parser, CompanyPrintParser

companies_route = Blueprint('companies', __name__)
companies_logger = init_logger('companies_logger')
companies_logger.setLevel(logging.INFO)


@companies_route.get('/admin/companies')
@login_required
async def get_companies(user: User):

    context: dict[str, str] = user.dict() if user else {}
    companies_controller = CompaniesController()
    companies: list[Company] = await companies_controller.get_user_companies(user_id=user.user_id)
    companies_dict = [company.dict() for company in companies if company] if isinstance(companies, list) else []

    notifications: NotificationsModel = await notifications_controller.get_user_notifications(user_id=user.user_id)
    notifications_dicts = [notice.dict() for notice in notifications.unread_notification] if notifications else []

    context.update(dict(companies=companies_dict, notifications_list=notifications_dicts))

    return render_template('companies/companies.html', **context)


@companies_route.get('/admin/company/<string:company_id>')
@login_required
async def get_company(user: User, company_id: str):
    user_data = user.dict()
    companies_controller = CompaniesController()
    company: Company = await companies_controller.get_company(company_id=company_id, user_id=user.user_id)
    properties: list[Property] = await companies_controller.get_properties(user=user, company_id=company_id)

    bank_accounts: BusinessBankAccount = await companies_controller.get_bank_accounts(user=user, company_id=company_id)

    properties_dict = [prop.dict() for prop in properties if prop] if isinstance(properties, list) else []
    bank_accounts_dicts = bank_accounts.dict() if bank_accounts else {}

    notifications: NotificationsModel = await notifications_controller.get_user_notifications(user_id=user.user_id)
    notifications_dicts = [notice.dict() for notice in notifications.unread_notification] if notifications else []

    context = dict(user=user_data,
                   company=company.dict() if isinstance(company, Company) else {},
                   properties=properties_dict,
                   bank_account=bank_accounts_dicts,
                   notifications_list=notifications_dicts)

    return render_template('companies/company.html', **context)


@companies_route.get('/admin/create-company')
@login_required
async def get_create_company(user: User):
    user_data = user.dict()
    notifications: NotificationsModel = await notifications_controller.get_user_notifications(user_id=user.user_id)

    notifications_dicts = [notice.dict() for notice in notifications.unread_notification] if notifications else []

    context = dict(user=user_data, notifications_list=notifications_dicts)

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


@companies_route.post('/admin/edit-company/<string:company_id>')
@login_required
async def do_edit_company(user: User, company_id: str):
    """

    :param user:
    :param company_id:
    :return:
    """
    try:
        company_data: UpdateCompany = UpdateCompany(**request.form)
    except ValidationError:
        message: str = "Error cannot update Company Data, Invalid Fields"
        flash(message=message, category="danger")
        return redirect(url_for('companies.get_company', company_id=company_id))

    company_controller = CompaniesController()
    _ = await company_controller.update_company(user=user, company_data=company_data)
    flash(message="Successfully Updated Company Data", category="success")
    return redirect(url_for('companies.get_company', company_id=company_id))


@companies_route.post('/admin/company/add-bank-account/<string:company_id>')
@login_required
async def do_add_bank_account(user: User, company_id: str):
    try:
        bank_account_details: BusinessBankAccount = BusinessBankAccount(**request.form)
        if company_id != bank_account_details.company_id:
            flash(message='Ouch That one hurt ', category="danger")
            return redirect(url_for('home.get_home'))
        companies_controller = CompaniesController()
        account_details = await companies_controller.update_bank_account(user=user,
                                                                         account_details=bank_account_details)
        companies_logger.info(account_details)

        flash(message="successfully updated company bank account details", category="success")

    except ValidationError as e:
        companies_logger.error(str(e))
        flash(message="Error creating Bank Account please fill in all the details", category="danger")

    return redirect(url_for('companies.get_company', company_id=company_id))


@companies_route.get('/admin/company/print/<string:company_id>')
@login_required
async def print_company(user: User, company_id: str):
    """

    :param user:
    :param company_id:
    :return:
    """
    user_id = user.user_id
    companies_controller = CompaniesController()
    company_data: Company = await companies_controller.get_company(company_id=company_id,
                                                                   user_id=user_id)
    company_bank_account: BusinessBankAccount = await companies_controller.get_bank_accounts(user=user,
                                                                                             company_id=company_id)
    properties_list: list[Property] = await companies_controller.get_properties(user=user,
                                                                                company_id=company_id)

    _title = f"{company_data.company_name.upper()} Report"

    company_data: CompanyPrintParser = map_company_to_parser(company=company_data)
    company_data_dict = {}
    if company_bank_account:
        bank_account_data: BankAccountPrintParser = BankAccountPrintParser(**company_bank_account.dict())
        company_data_dict.update({"Bank Account": bank_account_data.to_dict()})

    company_data_dict.update(company_data.to_dict())
    properties_dict = [building.dict() for building
                       in properties_list if building] if isinstance(properties_list, list) else []
    company_data_dict.update({"Properties": properties_dict})

    document_buffer = create_report(title=_title, data=company_data_dict)

    return send_file(
        path_or_file=document_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"{_title}.pdf")
