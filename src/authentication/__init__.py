from functools import wraps
from flask import Flask, request, render_template, redirect, url_for

from src.database.models.users import User

app = Flask(__name__)


# Your route handlers go here

async def get_user_details(user_id: str) -> User:
    # Implementation of retrieving user details
    pass


def login_required(route_function):
    @wraps(route_function)
    async def decorated_function(*args, **kwargs):
        auth_cookie = request.cookies.get('auth')
        if auth_cookie:
            # Assuming you have a function to retrieve the user details based on the user_id
            user = await get_user_details(auth_cookie)
            return route_function(user, *args, **kwargs)  # Inject user as a parameter
        return redirect(url_for('auth.get_login'))  # Redirect to login page if not logged in

    return decorated_function
