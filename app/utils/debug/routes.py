from flask import current_app as app
from flask import redirect, url_for
from flask_login import login_required, current_user

from ...models import db
from ...models.user import User


@app.route('/reset_password')
@login_required
def reset_password():
    current_user.set_password('test')
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/reset_password/<username>')
def reset_password_username(username: str):
    user = User.query.filter_by(username=username).first()
    user.set_password('test')
    db.session.commit()
    return redirect(url_for('index'))

# vim: ft=python ts=4 sw=4 sts=4 et
