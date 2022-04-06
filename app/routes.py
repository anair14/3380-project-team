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
                    ChangeEmailForm,
                    EmptyForm)
from .json_info import load_exercise
from .json_info import load_mealplans


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
            flash('Invalid username or password.', 'danger')
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
            profile_completed=False,
            exercise_weight_id = [],
            exercise_weight = []
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
        current_user.last_name = form.last_name.data
        current_user.birthdate = form.birthdate.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.profile_completed = True
        db.session.commit()
        flash('Changes have been saved.', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.birthdate.data = current_user.birthdate
        form.height.data = current_user.height
        form.weight.data = current_user.weight
    return render_template('forms/edit_profile.html', title='Edit Profile',
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
        'forms/change_password.html', title='Change Password', form=form
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
        'forms/change_email.html', title='Change Email', form=form
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
        'forms/change_username.html', title='Change Username', form=form
    )


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)


@app.route('/meal/<meal_id>')
@login_required
@complete_profile_required
def meal(meal_id: int):
    return render_template('index.html', title=f'Meal: {meal_id}')


@app.route('/meals')
@login_required
@complete_profile_required
def meals():
    return render_template('meals.html', title='Meals',
                            user = current_user, current = load_mealplans.getmealplan(current_user.get_mealplan()), mealplans = load_mealplans.getmealplans())


@app.route('/exercises', methods=['GET','POST'])
@login_required
@complete_profile_required
def exercises():
    if request.method == 'POST':
        sw = request.form.get('action1')
        print(sw)
        #current_user.setexercise(load_exercise.getexercise_basedonname(sw).getid())
        return exercise(load_exercise.getexercise_basedonname(sw).getid())
    #current_user.set_exercise_weight(1, 140)
    else:
        return render_template('exercises.html', title='Exercises',
                           user=current_user, current = load_exercise.getexercise(current_user.get_exercise()), exercises = load_exercise.getexercises(), weights = current_user.get_exercise_weights())


@app.route('/exercise/<exercise_id>')
@login_required
@complete_profile_required
def exercise(exercise_id: int):
    print("here")
    return render_template('exercise.html', title=f'Exercise: {exercise_id}', 
                            user = current_user, exercise = load_exercise.getexercise(exercise_id))

# @app.route('/setexercise', methods=['GET','POST'])
# @login_required
# @complete_profile_required
# def setmeal():
#     if request.method == 'POST':
#         sw = request.form.get('action1')
#         current_user.setexercise(load_exercise.getexercise_basedonname(sw).getid())
#         # if sw == 'Bicep Curls':
#         #     current_user.setexercise(load_exercise.getexercise_basedonname('Bicep Curls').getid())
#         # elif sw == 'Kettlebell Swing':
#         #     current_user.setexercise(load_exercise.getexercise_basedonname('Kettlebell Swing').getid())
#         # elif sw == 'Goblet Squats':
#         #     current_user.setexercise(load_exercise.getexercise_basedonname('Goblet Squats').getid())
#         # elif sw == 'Deadlifts':
#         #     current_user.setexercise(load_exercise.getexercise_basedonname('Deadlifts').getid())
#         # elif sw == 'Kettlebell Swing':
#         #     current_user.setexercise(load_exercise.getexercise_basedonname('Kettlebell Swing').getid())
#         # elif sw == 'Goblet Squats':
#         #     current_user.setexercise(load_exercise.getexercise_basedonname('Goblet Squats').getid())
#         # elif sw == 'Pendulum Lunges':
#         #     current_user.setexercise(load_exercise.getexercise_basedonname('Pendulum Lunges').getid())
#         # elif sw == 'Deadlifts':
#         #     current_user.setexercise(load_exercise.getexercise_basedonname('Deadlifts').getid())
#         # elif sw == 'Leg Extensions':
#         #     current_user.setexercise(load_exercise.getexercise_basedonname('Leg Extensions').getid())
#     return render_template('exercises.html', title='Exercises',
#                            user=current_user, current = load_exercise.getexercise(current_user.get_exercise()), exercises = load_exercise.getexercises(), weights = current_user.get_exercise_weights())


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username), 'danger')
            return redirect(url_for('index'))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username), 'success')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username), 'danger')
            return redirect(url_for('index'))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username), 'success')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/user/<username>/followers')
def followers_list(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    followers = user.followers
    return render_template(
        'followers.html', title='Followers', followers=followers
    )


@app.route('/user/<username>/followed')
def followings_list(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    followed = user.followed
    return render_template(
        'followed.html', title='Followed', followed=followed
    )



# vim: ft=python ts=4 sw=4 sts=4
