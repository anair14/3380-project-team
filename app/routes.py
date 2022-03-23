from flask import current_app as app
from flask import render_template, redirect, flash, url_for
from flask_login import (current_user,
                         login_user,
                         logout_user,
                         login_required)

from .models import db
from .models.user import User
from .utils import complete_profile_required
from .forms import RegistrationForm, LoginForm, EditProfileForm, EditAccountForm


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
@login_required
def logout():
    logout_user()
    return render_template('index.html', title='Logout')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index', title='Already registered.'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    profile_completed=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('edit_profile'))
    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
@complete_profile_required
def profile():
    return redirect(url_for('user', username=current_user.username))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = EditAccountForm()
    return render_template(
        'edit_account.html', title='Edit Account', form=form
    )


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/meal/<meal_id>')
@login_required
@complete_profile_required
def meal(meal_id: int):
    return render_template('index.html', title=f'Meal: {meal_id}')


@app.route('/meals')
@login_required
@complete_profile_required
def meals():
    return render_template('index.html', title='Meals')


@app.route('/exercise/<exercise_id>')
@login_required
@complete_profile_required
def exercise(exercise_id: int):
    return render_template('index.html', title=f'Exercise: {exercise_id}')


@app.route('/exercises')
@login_required
@complete_profile_required
def exercises():
    return render_template('index.html', title='Exercises')


@app.route('/toggle_profile_complete')
@login_required
def toggle_profile_complete():
    current_user.profile_completed = not current_user.profile_completed
    db.session.commit()
    return redirect(url_for('index'))

# vim: ft=python ts=4 sw=4 sts=4
