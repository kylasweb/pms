from flask import Blueprint, render_template, flash, redirect, url_for, request
from pydantic import ValidationError

from src.database.models.notifications import NotificationsModel
from src.main import company_controller, notifications_controller
from src.database.models.properties import Property, Unit, AddUnit, UpdateProperty, CreateProperty
from src.database.models.companies import Company
from src.database.models.users import User
from src.authentication import login_required

notices_route = Blueprint('notices', __name__)


@notices_route.get('/admin/notifications')
@login_required
async def get_all(user: User):
    """
    :return:
    """
    notifications_list: NotificationsModel = await notifications_controller.get_user_notifications(user_id=user.user_id)

    notifications_dicts = [notice.dict() for notice in notifications_list.all_notifications] if notifications_list else []

    return render_template('notifications/notifications_all.html', notifications_list=notifications_dicts)
