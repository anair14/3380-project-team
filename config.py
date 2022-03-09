class Default:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class Development(Default):
    SECRET_KEY = 'secret'
    TESTING = True
