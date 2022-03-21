from flask import current_app as app
from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user
from .forms import RegistrationForm, LoginForm
from .models import db
from .models.user import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html', title='Logout')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index', title='Already registered.'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    pass


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
