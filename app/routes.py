from flask import current_app as app

@app.route('/')
def index():
    return f'Hello, index.'

# vim: ft=python ts=4 sw=4 sts=4
