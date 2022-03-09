import os

from app import create_app

if os.environ.get('FLASK_ENV') == 'development':
    app = create_app('config.Development')
else:
    app = create_app('config.Default')

if __name__ == '__main__':
    app.run()
