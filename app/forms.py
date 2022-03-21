from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     BooleanField,
                     SubmitField,
                     DateField,
                     FloatField)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models.user import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username) -> None:
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Username already taken.')

    def validate_email(self, email) -> None:
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            raise ValidationError('Email address already taken.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField()
    last_name = StringField()
    birthdate = DateField()
    height = FloatField()
    weight = FloatField()

# vim: ft=python ts=4 sw=4 sts=4 et
