from .app import *
from flask import Flask


def flask_builder():
    app = Flask(__name__)

    with app.app_context():

        # db stuff
        pass

    return app


if __name__ == '__main__':
    app = flask_builder()

# vim: ft=python ts=4 sw=4 sts=4
