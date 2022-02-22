from flask import Flask


def flask_builder():
    app = Flask(__name__)
    with app.context():
        from app.routes import index
    return app


# vim: ft=python ts=4 sw=4 sts=4
