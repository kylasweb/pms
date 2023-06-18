from flask import Blueprint, render_template
from src.authentication import login_required
from src.database.models.users import User

statements_route = Blueprint('statements', __name__)


@statements_route.get('/admin/statements')
@login_required
async def get_statements(user: User):
    return render_template('statements/statements.html')

