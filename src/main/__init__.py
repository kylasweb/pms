from flask import Flask
from flask_bcrypt import Bcrypt
from src.firewall import Firewall
from src.utils import template_folder, static_folder

bcrypt = Bcrypt()

firewall = Firewall()

def bootstrapper():
    from src.database.sql.address import AddressORM
    from src.database.sql.tenants import TenantORM
    from src.database.sql.user import UserORM
    from src.database.sql.companies import UserCompanyORM, CompanyORM
    from src.database.sql.properties import PropertyORM, UnitORM

    AddressORM.create_if_not_table()
    TenantORM.create_if_not_table()
    UserORM.create_if_not_table()
    UserCompanyORM.create_if_not_table()
    CompanyORM.create_if_not_table()

    PropertyORM.create_if_not_table()
    UnitORM.create_if_not_table()


def create_app(config):
    app: Flask = Flask(__name__)

    app.template_folder = template_folder()
    app.static_folder = static_folder()
    app.config['SECRET_KEY'] = config.SECRET_KEY
    bcrypt.init_app(app=app)
    with app.app_context():

        firewall.init_app(app=app)

        from src.routes.home import home_route
        from src.routes.companies import companies_route
        from src.routes.buildings import buildings_route
        from src.routes.maintenance import maintenance_route
        from src.routes.reports import reports_route
        from src.routes.payments import payments_route
        from src.routes.invoices import invoices_route
        from src.routes.statements import statements_route
        from src.routes.auth import auth_route


        app.register_blueprint(home_route)
        app.register_blueprint(companies_route)
        app.register_blueprint(buildings_route)
        app.register_blueprint(maintenance_route)
        app.register_blueprint(reports_route)
        app.register_blueprint(payments_route)
        app.register_blueprint(invoices_route)
        app.register_blueprint(statements_route)
        app.register_blueprint(auth_route)

        bootstrapper()

    return app
