from flask import Blueprint, render_template, flash, redirect, url_for, request
from pydantic import ValidationError

from src.database.models.tenants import Tenant
from src.database.models.notifications import NotificationsModel
from src.main import company_controller, notifications_controller, tenant_controller
from src.database.models.properties import Property, Unit, AddUnit, UpdateProperty, CreateProperty
from src.database.models.companies import Company
from src.database.models.users import User
from src.authentication import login_required

buildings_route = Blueprint('buildings', __name__)


async def get_common_context(user: User, building_id: str, property_editor: bool = False):
    user_data = user.dict()
    building_property: Property = await company_controller.get_property(user=user, property_id=building_id)
    property_units: list[Unit] = await company_controller.get_property_units(user=user, property_id=building_id)
    notifications: NotificationsModel = await notifications_controller.get_user_notifications(user_id=user.user_id)

    notifications_dicts = [notice.dict() for notice in notifications.unread_notification] if notifications else []

    context = dict(
        user=user_data,
        property=building_property.dict(),
        property_editor=property_editor,
        notifications_list=notifications_dicts,
        units=[unit.dict() for unit in property_units]
    )
    return context


@buildings_route.get('/admin/buildings')
@login_required
async def get_buildings(user: User):
    user_data = user.dict()
    notifications: NotificationsModel = await notifications_controller.get_user_notifications(user_id=user.user_id)

    notifications_dicts = [notice.dict() for notice in notifications.unread_notification] if notifications else []

    context = dict(user=user_data, notifications_list=notifications_dicts)
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
    context = await get_common_context(user=user, building_id=building_id)
    return render_template('building/building.html', **context)


@buildings_route.get('/admin/add-building/<string:company_id>')
@login_required
async def add_building(user: User, company_id: str):
    user_data = user.dict()

    company: Company = await company_controller.get_company(company_id=company_id, user_id=user.user_id)
    notifications: NotificationsModel = await notifications_controller.get_user_notifications(user_id=user.user_id)

    notifications_dicts = [notice.dict() for notice in notifications.unread_notification] if notifications else []

    context = dict(user=user_data,
                   company=company.dict(), notifications_list=notifications_dicts)

    return render_template('building/add_building.html', **context)


@buildings_route.post('/admin/add-building/<string:company_id>')
@login_required
async def do_add_building(user: User, company_id: str):
    _ = user.dict()

    company: Company = await company_controller.get_company(company_id=company_id, user_id=user.user_id)
    property_data: CreateProperty = CreateProperty(**request.form)
    property_data.company_id = company.company_id
    property_model: Property = await company_controller.add_property(user=user, _property=property_data)

    _message: str = f"Property : {property_model.name.title()} Successfully added to : {company.company_name.title()}"
    flash(message=_message, category="success")
    return redirect(url_for('companies.get_company', company_id=company.company_id))


@buildings_route.get('/admin/edit-building/<string:building_id>')
@login_required
async def edit_building(user: User, building_id: str):
    context = await get_common_context(user, building_id, property_editor=True)
    return render_template('building/building.html', **context)


@buildings_route.post('/admin/edit-building/<string:building_id>')
@login_required
async def do_edit_building(user: User, building_id: str):
    try:
        updated_building: UpdateProperty = UpdateProperty(**request.form)
        _property = await company_controller.update_property(user=user, property_details=updated_building)
        if _property is not None:
            flash(message="Successfully updated Property/Building", category="success")
    except ValidationError as e:
        print(f"error {str(e)}")
        flash(message="Error updating Property/Building...", category="danger")

    context = await get_common_context(user=user, building_id=building_id)
    return render_template('building/building.html', **context)


@buildings_route.post('/admin/add-unit/<string:building_id>')
@login_required
async def do_add_unit(user: User, building_id: str):
    _ = user.dict()
    try:
        unit_data: AddUnit = AddUnit(**request.form)

        _ = await company_controller.add_unit(user=user, unit_data=unit_data, property_id=building_id)
        flash(message="Unit Added Successfully", category="success")
    except ValidationError as e:
        flash(message="To Add a Unit please Fill in all Fields", category="danger")
    return redirect(url_for('buildings.get_building', building_id=building_id))


@buildings_route.get('/admin/building/<string:building_id>/unit/<string:unit_id>')
@login_required
async def get_unit(user: User, building_id: str, unit_id: str):

    unit_data: Unit = await company_controller.get_unit(user=user, building_id=building_id, unit_id=unit_id)
    tenants_list: list[Tenant] = await tenant_controller.get_un_booked_tenants()

    if unit_data is None:
        flash(message="Could not find Unit with that ID", category="danger")
        redirect(url_for('buildings.get_building', building_id=building_id))

    context = {'unit': unit_data, 'tenants': tenants_list}
    return render_template('building/units/unit.html', **context)


