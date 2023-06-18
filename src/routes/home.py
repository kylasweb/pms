from flask import Blueprint, render_template

from src.database.models.users import User
from src.authentication import user_details

home_route = Blueprint('home', __name__)


@home_route.get('/')
@user_details
async def get_home(user: User):
    if user:
        user_data = user.dict()
        context = dict(user=user_data)
    else:
        context = {}

    return render_template('index.html', **context)
