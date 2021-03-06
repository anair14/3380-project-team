from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_mail import Mail

from .models import db, migrate
from .models.user import User


def create_app(config: str = None) -> Flask:
    """
    Flask factory function used to create a new instance of the app from a
    configuration file.

    :param config: config file to be loaded
    :return: flask app create with configuration from file
    """

    app = Flask(__name__)
    app.config.from_object(config)

    bootstrap = Bootstrap5()
    login = LoginManager()
    mail = Mail()
    login.user_loader(User.loader)
    login.login_view = "login"

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from . import routes
        if app.debug:
            from .utils.debug import routes

    return app

# vim: ft=python ts=4 sw=4 sts=4
