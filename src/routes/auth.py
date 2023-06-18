from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, make_response, flash, redirect, url_for
from src.database.models.users import User
from src.view.auth import UserView

auth_route = Blueprint('auth', __name__)


@auth_route.get('/admin/login')
async def get_login():
    return render_template('login.html')


@auth_route.post('/admin/login')
async def do_login():
    """
    Handle the login request.
    :return: The authenticated User object.
    """
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember')

    auth_view = UserView()
    login_user = await auth_view.login(username=username, password=password)

    if login_user and login_user.username == username:
        # Authentication successful
        # Render the companies.html template
        response = make_response(render_template('companies/companies.html'))
        # Calculate expiration time (e.g., 30 minutes from now)

        delay = timedelta(days=30) if remember == "on" else timedelta(minutes=30)
        expiration = datetime.utcnow() + delay
        # Set the authentication cookie
        response.set_cookie('auth', value=login_user.user_id, expires=expiration, httponly=True)
        # Return the response
        return response
    else:
        # Authentication failed
        # Add your desired logic here for failed login
        flash('Login failed. Please try again.')  # Flash the failure message
        return redirect(url_for('home.get_home'))


@auth_route.get('/admin/logout')
async def do_logout():
    """
    Handle the logout request.
    :return: Redirect to the home page.
    """
    # Create a response object
    response = make_response(redirect(url_for('home.get_home')))

    # Remove the session cookie
    response.delete_cookie('auth')

    # Flash the success message
    flash('You have been successfully logged out.')

    # Return the response
    return response


@auth_route.get('/admin/register')
async def get_register():
    return render_template('register.html')


@auth_route.post('/admin/register')
async def do_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # user_id will already be created by a factory
    user_data = User()
    user_data.username = username
    user_data.password = password
    user_data.email = email
    user_view = UserView()
    user_data: User = await user_view.post(user=user_data)

    response = make_response(render_template('companies/companies.html'))
    # Calculate expiration time (e.g., 30 minutes from now)
    expiration = datetime.utcnow() + timedelta(minutes=30)
    # Set the authentication cookie
    response.set_cookie('auth', value=user_data.user_id, expires=expiration, httponly=True)
    # Return the response
    return response


@auth_route.get('/admin/password-reset')
async def get_password_reset():
    return render_template('password_reset.html')
