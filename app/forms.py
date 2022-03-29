from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     BooleanField,
                     SubmitField,
                     DateField,
                     FloatField)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, NumberRange
from .models.user import User


def validate_username(self, username) -> None:
    user = User.query.filter_by(username=self.username.data).first()
    if user is not None:
        raise ValidationError('Username already taken.')


def validate_email(self, email) -> None:
    user = User.query.filter_by(email=self.email.data).first()
    if user is not None:
        raise ValidationError('Email address already taken.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), validate_username]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Email(), validate_email]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')


class EditProfileForm(FlaskForm):
    first_name = StringField(validators=[Length(min=1)])
    last_name = StringField(validators=[Length(min=1)])
    birthdate = DateField()
    # how do we handle height? convert a string to integer values?
    # what units are we using?
    height = FloatField()
    weight = FloatField(validators=[NumberRange(min=0)])
    submit = SubmitField('Update Profile')


class EditAccountForm(FlaskForm):
    username = StringField('Username', validators=[validate_username])
    new_password = PasswordField()
    new_password_repeat = PasswordField()
    old_password = PasswordField()
    email = StringField()
    new_email = StringField()

# vim: ft=python ts=4 sw=4 sts=4 et
