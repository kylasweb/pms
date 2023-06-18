from flask import Blueprint, render_template, flash, redirect, url_for

from src.database.models.properties import Property
from src.database.models.companies import Company
from src.database.models.users import User
from src.authentication import login_required
from src.view.companies import CompaniesView

buildings_route = Blueprint('buildings', __name__)


@buildings_route.get('/admin/buildings')
@login_required
async def get_buildings(user: User):

    user_data = user.dict()
    context = dict(user=user_data)
    # TODO load company data based on user data
    return render_template('building/buildings.html', **context)


@buildings_route.get('/admin/building/<string:building_id>')
@login_required
async def get_building(user: User, building_id: str):
    """
        returns a specific building by building id
    :param user:
    :param building_id:
    :return:
    """
    user_data = user.dict()
    context = dict(user=user_data)

    return render_template('building/building.html', **context)


@buildings_route.get('/admin/add-building/<string:company_id>')
@login_required
async def add_building(user: User, company_id: str):
    user_data = user.dict()
    company_view = CompaniesView()
    company: Company = await company_view.get_company(company_id=company_id, user_id=user.user_id)
    context = dict(user=user_data, company=company.dict())
    # TODO load company data based on user data

    return render_template('building/add_building.html', **context)


from flask import request


@buildings_route.post('/admin/add-building/<string:company_id>')
@login_required
async def do_add_building(user: User, company_id: str):
    user_data = user.dict()
    company_view = CompaniesView()
    company: Company = await company_view.get_company(company_id=company_id, user_id=user.user_id)
    property_data: Property = Property(**request.form)
    property_data.company_id = company.company_id
    property_model = await company_view.add_property(_property=property_data)

    _message: str = f"Property : {property_model.name} Successfully added to : {company.company_name}"
    flash(message=_message, category="success")
    return redirect(url_for('companies.get_company', company_id=company.company_id))
