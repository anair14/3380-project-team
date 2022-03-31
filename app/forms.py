from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     BooleanField,
                     SubmitField,
                     DateField,
                     FloatField,
                     EmailField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                NumberRange,
                                Optional)
from .models.user import User
from .utils.form_validators import (validate_email,
                                    validate_username,
                                    validate_password,
                                    validate_new_password,
                                    validate_new_username, validate_new_email)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), validate_username]
    )

    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), validate_email]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=4)]
    )

    password_repeat = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')]
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


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'Current Password',
        validators=[DataRequired(), validate_password]
    )

    new_password = PasswordField(
        'New Password',
        validators=[
            Length(min=4),
            validate_new_password
        ]
    )

    confirm_new_password = PasswordField(
        'Repeat New Password',
        validators=[EqualTo('new_password')]
    )

    submit = SubmitField('Change Password')


class ChangeEmailForm(FlaskForm):
    password = PasswordField(
        'Current Password',
        validators=[DataRequired(), validate_password]
    )

    new_email = EmailField(
        'New Email',
        validators=[Email(), Optional(), validate_new_email]
    )

    new_email_repeat = EmailField(
        'Repeat New Email',
        validators=[EqualTo('new_email'), Email()]
    )

    submit = SubmitField('Change Email')


class ChangeUsernameForm(FlaskForm):
    password = PasswordField(
        'Current Password',
        validators=[DataRequired(), validate_password]
    )

    new_username = StringField(
        'New Username',
        validators=[Optional(), validate_new_username]
    )

    submit = SubmitField('Change Username')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# vim: ft=python ts=4 sw=4 sts=4 et
