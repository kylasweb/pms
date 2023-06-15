from flask import Blueprint, render_template

buildings_route = Blueprint('buildings', __name__)


@buildings_route.get('/admin/buildings')
async def get_buildings():
    return render_template('building/buildings.html')


@buildings_route.get('/admin/building/<string:building_id>')
async def get_building(building_id: str):
    """
        returns a specific building by building id
    :param building_id:
    :return:
    """
    return render_template('building/building.html')


@buildings_route.get('/admin/add-building')
async def add_building():
    return render_template('building/add_building.html')
