from flask import Flask
from flask_bootstrap import Bootstrap


def flask_builder():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////./data/app.db'

    bootstrap = Bootstrap()

    from .model import db
    from .navigation import nav

    db.init_app(app)
    nav.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        from .routes import index

    return app

# vim: ft=python ts=4 sw=4 sts=4
