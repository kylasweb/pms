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

    if login_user and login_user.get('username') == username:
        # Authentication successful
        # Render the companies.html template
        response = make_response(redirect(url_for('companies.get_companies')))
        # Calculate expiration time (e.g., 30 minutes from now)

        delay = timedelta(days=30) if remember == "on" else timedelta(minutes=30)
        expiration = datetime.utcnow() + delay
        # Set the authentication cookie
        response.set_cookie('auth', value=login_user.get('user_id'), expires=expiration, httponly=True)
        # Return the response
        return response
    else:
        # Authentication failed
        # Add your desired logic here for failed login
        flash(message='Login failed. Please try again.', category="danger")  # Flash the failure message
        return redirect(url_for('auth.get_login'))


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
    flash(message='You have been successfully logged out.', category="danger")

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
    terms = request.form.get('terms')

    if not (username and email and password):
        flash(message="Please fill in all the required fields.", category="danger")
        return make_response(redirect(url_for('auth.get_register')))

    if terms != "on":
        flash(message="please accept terms and conditions", category="danger")
        return make_response(redirect(url_for('auth.get_register')))

    user_view = UserView()

    user_exist = await user_view.get_by_email(email=email)
    if user_exist:
        flash(message="User Already Exist please login", category="success")
        return make_response(redirect(url_for('auth.get_login')))

    # user_id will already be created by a factory
    user_data = User(**dict(username=username, password=password, email=email))

    _user_data: dict[str, str | bool] = await user_view.post(user=user_data)
    flash(message="Successfully logged in", category="success")
    response = make_response(redirect(url_for('companies.get_companies')))
    # Calculate expiration time (e.g., 30 minutes from now)
    expiration = datetime.utcnow() + timedelta(minutes=30)
    # Set the authentication cookie
    response.set_cookie('auth', value=_user_data.get('user_id'), expires=expiration, httponly=True)
    # Return the response
    return response


@auth_route.get('/admin/password-reset')
async def get_password_reset():
    return render_template('password_reset.html')


@auth_route.post('/admin/password-reset')
async def do_password_reset():
    email = request.form.get('email')
    if not email:
        flash(message="please submit an email in order to proceed with password reset", category="danger")
        return make_response(redirect(url_for('auth.get_password_reset')))

    flash(message="password reset email sent to your Inbox", category='success')
    return make_response(redirect(url_for('home.get_home')))
