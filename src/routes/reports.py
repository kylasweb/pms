from flask import Blueprint, render_template

reports_route = Blueprint('reports', __name__)


@reports_route.get('/admin/reports')
async def get_reports():
    return render_template('reports/reports.html')

