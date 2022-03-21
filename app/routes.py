from flask import current_app as app, redirect, url_for
from flask import render_template
from .forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    return render_template('index.html', title='Logout')


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)


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
