from flask import current_app as app
from flask import (render_template,
                   redirect,
                   flash,
                   url_for,
                   request)
from flask_login import (current_user,
                         login_user,
                         logout_user,
                         login_required)

from .models import db
from .models.user import User
from .utils import complete_profile_required
from .forms import (RegistrationForm,
                    LoginForm,
                    EditProfileForm,
                    ChangePasswordForm,
                    ChangeUsernameForm,
                    ChangeEmailForm)


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
        user = User(
            username=form.username.data,
            email=form.email.data,
            profile_completed=False
        )
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
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.first_name.data
        current_user.birthdate = form.birthdate.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.profile_completed = True
        db.session.commit()
        flash('Changes have been saved.')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.birthdate.data = current_user.birthdate
        form.height.data = current_user.height
        form.weight.data = current_user.weight
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form, user=current_user)


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account', user=current_user)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        db.session.commit()

    return render_template(
        'change_password.html', title='Change Password', form=form
    )


@app.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()

    if form.validate_on_submit():
        current_user.email = form.new_email.data
        db.session.commit()
    elif request.method == 'GET':
        form.new_email.data = current_user.email
        form.new_email_repeat.data = current_user.email

    return render_template(
        'change_email.html', title='Change Email', form=form
    )


@app.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUsernameForm()

    if form.validate_on_submit():
        current_user.username = form.new_username.data
        db.session.commit()
    elif request.method == 'GET':
        form.new_username.data = current_user.username

    return render_template(
        'change_username.html', title='Change Username', form=form
    )


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/user/<username>/followers')
def followers_list(username: str):
    followers = current_user.followers
    return render_template(
        'follower.html', title='Followers', followers=followers
    )


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

# vim: ft=python ts=4 sw=4 sts=4
