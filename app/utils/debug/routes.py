from flask import current_app as app, flash
from flask import redirect, url_for
from flask_login import login_required, current_user

from ...models import db
from ...models.user import User


@app.route('/reset_password')
@login_required
def reset_password():
    """Debug function to reset the password for the current user to 'test'.
    """
    current_user.set_password('test')
    db.session.commit()
    flash('Password for current user set to "test".', 'info')
    return redirect(url_for('index'))


@app.route('/reset_password/<username>')
def reset_password_username(username: str):
    """Debug function to reset the password for user with given username to
    'test'.

    :param username: string username of the user
    """
    user = User.query.filter_by(username=username).first()
    user.set_password('test')
    db.session.commit()
    flash(f'Password for user {user.username} set to "test".', 'info')
    return redirect(url_for('index'))

# vim: ft=python ts=4 sw=4 sts=4 et
