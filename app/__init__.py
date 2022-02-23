from flask import Flask


def flask_builder():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////./data/app.db'

    from app.model import db
    db.init_app(app)

    with app.app_context():
        from app.routes import index


    return app


# vim: ft=python ts=4 sw=4 sts=4
