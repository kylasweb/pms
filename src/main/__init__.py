from os import path
from flask import Flask


def static_folder() -> str:
    return path.join(path.dirname(path.abspath(__file__)), '../../static')


def template_folder() -> str:
    return path.join(path.dirname(path.abspath(__file__)), '../../templates')


def create_app(config):
    app: Flask = Flask(__name__)

    app.template_folder = template_folder()
    app.static_folder = static_folder()
    app.config['SECRET_KEY'] = config.SECRET_KEY

    with app.app_context():
        from src.routes.home import home_route
        from src.routes.companies import companies_route
        from src.routes.buildings import buildings_route
        from src.routes.maintenance import maintenance_route
        from src.routes.reports import reports_route
        from src.routes.payments import payments_route
        from src.routes.invoices import invoices_route

        app.register_blueprint(home_route)
        app.register_blueprint(companies_route)
        app.register_blueprint(buildings_route)
        app.register_blueprint(maintenance_route)
        app.register_blueprint(reports_route)
        app.register_blueprint(payments_route)
        app.register_blueprint(invoices_route)


    return app
