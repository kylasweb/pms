from flask import Blueprint, render_template

statements_route = Blueprint('statements', __name__)


@statements_route.get('/admin/statements')
async def get_statements():
    return render_template('statements/statements.html')

