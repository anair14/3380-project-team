from flask import current_app as app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return 'Hello, index.'


@app.route('/login', methods=['GET', 'POST'])
def login():
    # will handle both logging in and registering new users
    pass


@app.route('/logout')
def logout():
    pass


@app.route('/user/<username>', methods=['GET', 'POST'])
def user():
    # handle editing and displaying profile
    pass


@app.route('/meal/<meal_id>')
def meal():
    pass


@app.route('/meals')
def meals():
    pass


@app.route('/exercise/<exercise_id>')
def exercise():
    pass


@app.route('/exercises')
def exercises():
    pass

# vim: ft=python ts=4 sw=4 sts=4
