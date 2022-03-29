from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import ValidationError
from flask_login import current_user
from ..models.user import User


def validate_username(self: FlaskForm, username: StringField) -> None:
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValidationError('Username already taken.')


def validate_email(self: FlaskForm, email: StringField) -> None:
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
        raise ValidationError('Email address already taken.')


def validate_password(self: FlaskForm, password: PasswordField) -> None:
    if not current_user.check_password(password.data):
        raise ValidationError('Please enter your current password.')


def validate_new_password(self: FlaskForm, new_password: PasswordField) -> None:
    # check password will return true if the new password
    # is the same as the old password
    if current_user.check_password(new_password.data):
        raise ValidationError(
            'New password cannot be the same as old password.'
        )

# vim: ft=python ts=4 sw=4 sts=4 et
