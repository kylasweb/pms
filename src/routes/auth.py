from flask import Blueprint, render_template, request

auth_route = Blueprint('auth', __name__)


@auth_route.get('/admin/login')
async def get_login():
    return render_template('login.html')


@auth_route.get('/admin/register')
async def get_register():
    return render_template('register.html')


@auth_route.get('/admin/password-reset')
async def get_password_reset():
    return render_template('password_reset.html')
