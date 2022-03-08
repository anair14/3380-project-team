from flask import current_app as app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html', title='Login')


@app.route('/logout')
def logout():
    return render_template('index.html', title='Logout')


@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username: str):
    return render_template('index.html', title=f'User: {username}')


@app.route('/meal/<meal_id>')
def meal(meal_id: int):
    return render_template('index.html', title=f'Meal: {meal_id}')


@app.route('/meals')
def meals():
    return render_template('index.html', title='Meals')


@app.route('/exercise/<exercise_id>')
def exercise(exercise_id: int):
    return render_template('index.html', title=f'Exercise: {exercise_id}')


@app.route('/exercises')
def exercises():
    return render_template('index.html', title='Exercises')

# vim: ft=python ts=4 sw=4 sts=4
