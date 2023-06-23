from flask import Blueprint, render_template

from src.main import notifications_controller
from src.database.models.notifications import NotificationsModel
from src.database.models.users import User
from src.authentication import user_details

home_route = Blueprint('home', __name__)


@home_route.get('/')
@user_details
async def get_home(user: User):
    if user:
        user_data = user.dict()
        notifications: NotificationsModel = await notifications_controller.get_user_notifications(user_id=user.user_id)
        notifications_dicts = [notice.dict() for notice in notifications.unread_notification]

        context = dict(user=user_data, notifications_list=notifications_dicts)

    else:
        context = {}
    return render_template('index.html', **context)
