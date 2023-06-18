from flask import Blueprint, render_template
from src.authentication import login_required
from src.database.models.users import User

reports_route = Blueprint('reports', __name__)


@reports_route.get('/admin/reports')
@login_required
async def get_reports(user: User):
    return render_template('reports/reports.html')

