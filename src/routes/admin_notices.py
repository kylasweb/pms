from flask import Blueprint, render_template, flash, redirect, url_for, request
from pydantic import ValidationError

from src.main import company_controller
from src.database.models.properties import Property, Unit, AddUnit, UpdateProperty, CreateProperty
from src.database.models.companies import Company
from src.database.models.users import User
from src.authentication import login_required

notices_route = Blueprint('notices', __name__)



@notices_route.get('/admin/user/<string:user_id>')
@login_required
def get_admin_notices(user: User, user_id: str):
    """

    :param user_id:
    :return:
    """




