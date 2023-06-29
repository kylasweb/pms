from flask import Blueprint, render_template, flash, redirect, url_for, request
from pydantic import ValidationError

from src.database.models.invoices import CreateInvoicedItem, BillableItem, CreateUserCharge
from src.logger import init_logger
from src.database.models.lease import LeaseAgreement, CreateLeaseAgreement
from src.database.models.tenants import Tenant
from src.database.models.notifications import NotificationsModel
from src.main import company_controller, notifications_controller, tenant_controller, lease_agreement_controller
from src.database.models.properties import Property, Unit, AddUnit, UpdateProperty, CreateProperty
from src.database.models.companies import Company
from src.database.models.users import User
from src.authentication import login_required

buildings_route = Blueprint('buildings', __name__)
buildings_logger = init_logger("Buildings-Router")


async def get_common_context(user: User, building_id: str, property_editor: bool = False):
    user_data = user.dict()
    building_property: Property = await company_controller.get_property(user=user, property_id=building_id)
    property_units: list[Unit] = await company_controller.get_property_units(user=user, property_id=building_id)
    notifications: NotificationsModel = await notifications_controller.get_user_notifications(user_id=user.user_id)

    notifications_dicts = [notice.dict() for notice in notifications.unread_notification] if notifications else []
    billable_items_: list[BillableItem] = await company_controller.get_billable_items(building_id=building_id)
    billable_dicts = [bill.dict() for bill in billable_items_ if bill and not bill.deleted] if billable_items_ else []

    context = dict(
        user=user_data,
        property=building_property.dict(),
        property_editor=property_editor,
        notifications_list=notifications_dicts,
        units=[unit.dict() for unit in property_units],
        billable_items=billable_dicts
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
    context = await get_common_context(user=user,
                                       building_id=building_id)

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
    billable_items_: list[BillableItem] = await company_controller.get_billable_items(building_id=building_id)
    billable_dicts: list[dict[str, str | int]] = [item.dict()
                                                  for item in billable_items_ if item] if billable_items else []
    if unit_data is None:
        flash(message="Could not find Unit with that ID", category="danger")
        redirect(url_for('buildings.get_building', building_id=building_id))

    context = {'unit': unit_data, 'tenants': tenants_list, 'billable_items': billable_dicts}
    return render_template('building/units/unit.html', **context)


@buildings_route.post('/admin/building/<string:building_id>/unit/<string:unit_id>')
@login_required
async def add_tenant_to_building_unit(user: User, building_id: str, unit_id: str):
    context = dict(user=user.dict())
    tenant_rental = Unit(**request.form)
    updated_unit = await company_controller.update_unit(user_id=user.user_id, unit_data=tenant_rental)

    if updated_unit:
        context.update(dict(unit=updated_unit.dict()))

    tenant: Tenant = await tenant_controller.get_tenant_by_id(tenant_id=tenant_rental.tenant_id)
    tenant.is_renting = True
    tenant.lease_start_date = tenant_rental.lease_start_date
    tenant.lease_end_date = tenant_rental.lease_end_date
    updated_tenant = await tenant_controller.update_tenant(tenant=tenant)

    if updated_tenant:
        context.update(dict(tenant=updated_tenant.dict()))

    deposit_amount = await lease_agreement_controller.calculate_deposit_amount(
        rental_amount=tenant_rental.rental_amount)

    lease_dict: dict[str, str] = dict(property_id=tenant_rental.property_id,
                                      tenant_id=tenant_rental.tenant_id,
                                      unit_id=tenant_rental.unit_id,
                                      start_date=tenant_rental.lease_start_date,
                                      end_date=tenant_rental.lease_end_date,
                                      rent_amount=tenant_rental.rental_amount,
                                      deposit_amount=deposit_amount,
                                      is_active=True)

    try:
        lease_: CreateLeaseAgreement = CreateLeaseAgreement(**lease_dict)
        lease: LeaseAgreement = await lease_agreement_controller.create_lease_agreement(lease=lease_)
    except ValidationError as e:
        buildings_logger.error(f"Error creating Lease Agreement : {str(e)}")
        flash(message=f"Validation error : {str(e)}", category="danger")
        return redirect(url_for('buildings.get_unit', building_id=building_id, unit_id=unit_id))
    if lease:
        context.update(dict())
    building_: Property = await company_controller.get_property_by_id_internal(property_id=building_id)
    building_.available_units -= 1
    updated_building: Property = await company_controller.update_property(user=user, property_details=building_)
    print(f'Updated Building : {updated_building}')
    if updated_building:
        context.update(dict(building=updated_building.dict()))

    flash(message='Lease Agreement created Successfully', category="success")
    return render_template('tenants/official/tenant_rental_result.html', **context)


@buildings_route.post('/admin/building/billable')
@login_required
async def billable_items(user: User):
    """

    :param user:
    :return:
    """
    billable_item: CreateInvoicedItem = CreateInvoicedItem(**request.form)
    print(f"BILLABLE ITEMS : {billable_item}")
    billable_item: CreateInvoicedItem = await company_controller.create_billable_item(billable_item=billable_item)
    flash(message="Billable Item Added to building", category="success")
    return redirect(url_for("buildings.get_building", building_id=billable_item.property_id))


@buildings_route.post('/admin/building/billed-item/<string:property_id>/<string:item_number>')
@login_required
async def get_billed_item(user: User, property_id: str, item_number: str):
    """

    :param user:
    :param property_id:
    :param item_number:
    :return:
    """
    billed_item: CreateInvoicedItem = company_controller.get_billed_item(property_id=property_id,
                                                                         item_number=item_number)
    return billed_item


@buildings_route.get('/admin/building/delete-billed-item/<string:property_id>/<string:item_number>')
@login_required
async def delete_billed_item(user: User, property_id: str, item_number: str):
    """

    :param user:
    :param property_id:
    :param item_number:
    :return:
    """
    billed_item: CreateInvoicedItem = await company_controller.delete_billed_item(property_id=property_id,
                                                                                  item_number=item_number)
    flash(message="Billable Item Deleted", category="success")
    return redirect(url_for("buildings.get_building", building_id=property_id))


@buildings_route.get('/admin/building/create-charge')
@login_required
async def create_billing_charge(user: User):
    """

    :param user:
    :return:

    """
    unit_charge_item: CreateUserCharge = CreateUserCharge(**request.form)
    created_bill = await company_controller.create_charge(charge_item=unit_charge_item)
    flash(message="Billing Charge Added to Unit", category="success")
    return redirect(url_for("buildings.get_building", building_id=unit_charge_item.property_id))
