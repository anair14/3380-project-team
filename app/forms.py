from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     BooleanField,
                     SubmitField,
                     DateField,
                     FloatField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                NumberRange)
from .models.user import User
from .utils.form_validators import (validate_email,
                                    validate_username,
                                    validate_password,
                                    validate_new_password)


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
    old_password = PasswordField(
        'Current Password', validators=[DataRequired(), validate_password]
    )
    new_username = StringField('Username', validators=[validate_username])
    new_password = PasswordField(
        'New Password', validators=[validate_new_password]
    )
    new_password_repeat = PasswordField(
        'Repeat New Password', validators=[EqualTo('new_password')]
    )
    new_email = StringField('New Email', validators=[validate_email])
    submit = SubmitField('Update Account')

# vim: ft=python ts=4 sw=4 sts=4 et
