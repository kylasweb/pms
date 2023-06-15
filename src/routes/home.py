from flask import Blueprint

home_route = Blueprint('home', __name__)


@home_route.get('/')
def get_home():
    return
