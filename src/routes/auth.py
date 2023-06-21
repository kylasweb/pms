from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, make_response, flash, redirect, url_for, Response
from pydantic import ValidationError

from src.logger import init_logger
from src.database.models.auth import Auth, RegisterUser
from src.database.models.users import User
from src.controller.auth import UserController

auth_route = Blueprint('auth', __name__)
auth_logger = init_logger('auth_logger')

REMEMBER_ME_DELAY = 60 * 60 * 24 * 30


async def create_response(redirect_url, message=None, category=None) -> Response:
    response = make_response(redirect(redirect_url))
    if message and category:
        flash(message=message, category=category)
    return response


@auth_route.get('/admin/login')
async def get_login():
    return render_template('login.html')


@auth_route.post('/admin/login')
async def do_login():
    auth_controller = UserController()
    try:
        auth_user = Auth(**request.form)
    except ValidationError as e:
        auth_logger.error(str(e))
        return await create_response(url_for('auth.get_login'), 'Login failed. Please try again.', 'danger')

    login_user = await auth_controller.login(username=auth_user.username, password=auth_user.password)
    if login_user and login_user.get('username') == auth_user.username:
        response = await create_response(url_for('companies.get_companies'))
        delay = REMEMBER_ME_DELAY if auth_user.remember == "on" else 30
        expiration = datetime.utcnow() + timedelta(minutes=delay)
        response.set_cookie('auth', value=login_user.get('user_id'), expires=expiration, httponly=True)
        return response
    else:
        return await create_response(url_for('auth.get_login'), 'Login failed. Please try again.', 'danger')


@auth_route.get('/admin/logout')
async def do_logout():
    response = await create_response(url_for('home.get_home'))
    response.delete_cookie('auth')
    flash(message='You have been successfully logged out.', category='danger')
    return response


@auth_route.get('/admin/register')
async def get_register():
    return render_template('register.html')


@auth_route.post('/admin/register')
async def do_register():
    try:
        register_user = RegisterUser(**request.form)
    except ValidationError as e:
        auth_logger.error(str(e))
        return await create_response(url_for('auth.get_register'), 'Please fill in all the required fields.', 'danger')

    user_controller = UserController()

    user_exist = await user_controller.get_by_email(email=register_user.email)
    if user_exist:
        flash(message='User Already Exist please login', category='success')
        return await create_response(url_for('auth.get_login'))

    user_data = User(**register_user.dict(exclude={'terms'}))

    _user_data = await user_controller.post(user=user_data)
    flash(message='Successfully logged in', category='success')
    response = await create_response(url_for('companies.get_companies'))
    expiration = datetime.utcnow() + timedelta(minutes=30)
    response.set_cookie('auth', value=_user_data.get('user_id'), expires=expiration, httponly=True)
    return response


@auth_route.get('/admin/password-reset')
async def get_password_reset():
    return render_template('password_reset.html')


@auth_route.post('/admin/password-reset')
async def do_password_reset():
    email = request.form.get('email')
    if not email:
        flash(message='Please submit an email in order to proceed with password reset', category='danger')
        return await create_response(url_for('auth.get_password_reset'))

    user_controller = UserController()
    email_exist = await user_controller.get_by_email(email=email)
    if email_exist is not None:
        await user_controller.send_password_reset(email=email)

    flash(message='Password reset email sent to your Inbox', category='success')
    return await create_response(url_for('home.get_home'))
