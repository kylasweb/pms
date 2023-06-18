from flask import Blueprint, render_template

from src.database.models.users import User
from src.authentication import login_required

buildings_route = Blueprint('buildings', __name__)


@buildings_route.get('/admin/buildings')
@login_required
async def get_buildings(user: User):
    return render_template('building/buildings.html')


@buildings_route.get('/admin/building/<string:building_id>')
@login_required
async def get_building(user: User, building_id: str):
    """
        returns a specific building by building id
    :param user:
    :param building_id:
    :return:
    """
    return render_template('building/building.html')


@buildings_route.get('/admin/add-building')
@login_required
async def add_building(user: User):
    return render_template('building/add_building.html')
