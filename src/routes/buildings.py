from flask import Blueprint, render_template, flash, redirect, url_for, request
from pydantic import ValidationError

from src.database.models.properties import Property, Unit, AddUnit, UpdateProperty
from src.database.models.companies import Company
from src.database.models.users import User
from src.authentication import login_required
from src.controller.companies import CompaniesController

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
    company_controller = CompaniesController()
    building_property: Property = await company_controller.get_property(property_id=building_id)
    property_units: list[Unit] = await company_controller.get_property_units(property_id=building_id)
    context = dict(user=user_data,
                   property=building_property.dict(),
                   property_editor=False,
                   units=[unit.dict() for unit in property_units])

    return render_template('building/building.html', **context)


@buildings_route.get('/admin/add-building/<string:company_id>')
@login_required
async def add_building(user: User, company_id: str):
    user_data = user.dict()
    company_controller = CompaniesController()
    company: Company = await company_controller.get_company(company_id=company_id, user_id=user.user_id)
    context = dict(user=user_data,
                   company=company.dict())

    return render_template('building/add_building.html', **context)


@buildings_route.post('/admin/add-building/<string:company_id>')
@login_required
async def do_add_building(user: User, company_id: str):
    _ = user.dict()
    company_controller = CompaniesController()
    company: Company = await company_controller.get_company(company_id=company_id, user_id=user.user_id)
    property_data: Property = Property(**request.form)
    property_data.company_id = company.company_id
    property_model = await company_controller.add_property(_property=property_data)

    _message: str = f"Property : {property_model.name} Successfully added to : {company.company_name}"
    flash(message=_message, category="success")
    return redirect(url_for('companies.get_company', company_id=company.company_id))


@buildings_route.get('/admin/edit-building/<string:building_id>')
@login_required
async def edit_building(user: User, building_id: str):
    user_data = user.dict()
    company_controller = CompaniesController()
    building: Property = await company_controller.get_property(property_id=building_id)

    property_units: list[Unit] = await company_controller.get_property_units(property_id=building_id)
    context = dict(user=user_data,
                   property_editor=True,
                   property=building.dict(),
                   units=[unit.dict() for unit in property_units])

    return render_template('building/building.html', **context)


@buildings_route.post('/admin/edit-building/<string:building_id>')
@login_required
async def do_edit_building(user: User, building_id: str):
    user_data = user.dict()

    updated_building: UpdateProperty = UpdateProperty(**request.form)

    company_controller = CompaniesController()
    building: Property = await company_controller.update_property(property_details=updated_building)
    property_units: list[Unit] = await company_controller.get_property_units(property_id=building_id)
    context = dict(user=user_data,
                   property_editor=False,
                   property=building.dict(),
                   units=[unit.dict() for unit in property_units])

    flash(message="Successfully updated Property/Building", category="success")
    return render_template('building/building.html', **context)


@buildings_route.post('/admin/add-unit/<string:building_id>')
@login_required
async def do_add_unit(user: User, building_id: str):
    _ = user.dict()
    try:
        unit_data: AddUnit = AddUnit(**request.form)
        company_controller = CompaniesController()
        _ = await company_controller.add_unit(unit_data=unit_data, property_id=building_id)
        flash(message="Unit Added Successfully", category="success")
    except ValidationError as e:
        flash(message="To Add a Unit please Fill in all Fields", category="danger")
    return redirect(url_for('buildings.get_building', building_id=building_id))
