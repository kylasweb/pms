from flask import Blueprint, render_template

home_route = Blueprint('home', __name__)


@home_route.get('/')
async def get_home():
    return render_template('index.html')
