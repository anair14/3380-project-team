from flask import Flask


def create_app(config: str = None) -> Flask:
    """
    Flask factory function used to create a new instance of the app from a
    configuration file.

    :param config: config file to be loaded
    :return: flask app create with configuration from file
    """

    app = Flask(__name__)
    app.config.from_object(config)

    from flask_bootstrap import Bootstrap
    from .models import db, migrate
    from .navigation import nav

    bootstrap = Bootstrap()

    db.init_app(app)
    migrate.init_app(app, db)
    nav.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        pass

    return app

# vim: ft=python ts=4 sw=4 sts=4
