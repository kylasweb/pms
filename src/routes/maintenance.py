from flask import Blueprint, render_template
from src.authentication import login_required
from src.database.models.users import User

maintenance_route = Blueprint('maintenance', __name__)


@maintenance_route.get('/admin/maintenance')
@login_required
async def get_maintenance(user: User):
    return render_template('maintenance/maintenance.html')
