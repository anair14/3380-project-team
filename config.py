from pathlib import Path
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQALCHEMY_TRACK_MODIFICATIONS = False
class Default:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class Development(Default):
    SECRET_KEY = 'secret'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(
        Path(__file__).parent / Path('data', 'app.db'))