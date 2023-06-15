from flask import Blueprint, render_template

maintenance_route = Blueprint('maintenance', __name__)


@maintenance_route.get('/admin/maintenance')
async def get_maintenance():
    return render_template('maintenance/maintenance.html')
