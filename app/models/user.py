from datetime import date
from typing import List

from flask import current_app as app
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

from . import db
from .followers import followers
from ..json_info import exercise

exerciseplan = exercise.ExercisePlan()


class User(UserMixin, db.Model):
    """SQLAlchemy model of user."""
    id = db.Column(db.Integer, primary_key=True)

    """Account Information
    
    Username and email address must both be unique, and cannot be null.
    """
    username = db.Column(
        db.String(150),
        index=True,
        unique=True,
        nullable=False
    )
    email = db.Column(db.String(150), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    """ Personal Information
    
    Information about a user.
    """
    profile_completed = db.Column(db.Boolean(), default=False, nullable=False)
    """profile_completed is used to determine if a user is able to access 
           features that require a height and weight """
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    birthdate = db.Column(db.Date())
    height = db.Column(db.Float())
    weight = db.Column(db.Float())

    current_exercise_id = db.Column(db.Integer())
    exercise_weight_id = db.Column(db.PickleType(), nullable=True)
    exercise_weight = db.Column(db.PickleType(), nullable=True)
    current_mealplan_id = db.Column(db.Integer())
    posts = db.relationship('Post', backref='author')

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref(
            'followers',
            lazy='dynamic'
        ),
        lazy='dynamic'
    )

    def __repr__(self):
        """String representation of user.

        :return: string representing the user
        """
        if app.debug:
            return f'<User {self.username},' \
                   f'id: {self.id},' \
                   f'current_exercise_id {self.current_exercise_id},' \
                   f'exercise_weight_id {self.exercise_weight_id},' \
                   f'exercise_weight {self.exercise_weight}> '
        return f'<User {self.username}, id: {self.id}>'

    def set_password(self, new_password: str) -> None:
        """Hashes new password and set's it.

        :param new_password: new password to be hashed and set
        """
        if app.debug:
            self.password_hash = generate_password_hash(
                new_password,
                method='plain'
            )
        else:
            self.password_hash = generate_password_hash(new_password)

    def check_password(self, password: str) -> bool:
        """Checks if password is equal to the user's current password.

        :param password: password to be checked against password_hash
        :return: true if the password hashes match, false otherwise
        """
        return check_password_hash(self.password_hash, password)

    @hybrid_property
    def age(self) -> int:
        """Calculates the user's age in years from birthdate.

        :return: integer age in years
        """
        today = date.today()
        return ((today.year - self.birthdate.year)
                - ((today.month, today.day)
                   < (self.birthdate.month, self.birthdate.day)))

    @staticmethod
    def loader(user_id: int) -> 'User':
        """Helper function for flask-login.
        Returns a user using id.

        :param user_id: integer id of the user to be returned
        :return: User model with id user_id
        """
        return User.query.get(int(user_id))

    def follow(self, user: 'User') -> None:
        """Follows another user if not already following.

        :param user: the user to be followed
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user: 'User') -> None:
        """Unfollows another user if already following.

        :param user: the user to be unfollowed
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user: 'User') -> bool:
        """Returns true if the following user.

        :param user: the user to be checked
        :return: true if current user is following user
        """
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def avatar(self, size: int) -> str:
        """Get avatar for the current user from Gravatar.

        :param size: size of the avatar in pixels
        :return: url for the current user's avatar
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        url = f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
        return url

    def set_exercise_weight(self, exercise_id, weight) -> None:
        """Set an exercise weight to a custom value.

        Saves an array of all the exercise ids whose weights have changed
        and another array that contains the actual weights of those exercises.

        :param exercise_id: the id of the exercise
        :param weight: the new weight for the exercise
        """
        # if array isn't initialized or empty
        if self.exercise_weight_id is None or self.exercise_weight_id == []:
            self.exercise_weight_id = [exercise_id]
            self.exercise_weight = [weight]
        else:
            # if we've already changed the weight once want to simply modify
            # our current weight array
            if exercise_id in self.exercise_weight_id:
                i = self.exercise_weight_id.index(exercise_id)
                # because db.pickletype saves a reference to the array,
                # cannot simply use append must create a new array through
                # concatenation and pop the old elements out
                self.exercise_weight_id = self.exercise_weight_id + [
                    exercise_id]
                self.exercise_weight = self.exercise_weight + [int(weight)]
                self.exercise_weight_id.pop(i)
                self.exercise_weight.pop(i)
            else:
                # because db.pickletype saves a reference to the array,
                # cannot simply use append
                self.exercise_weight_id = self.exercise_weight_id + [
                    exercise_id]
                self.exercise_weight = self.exercise_weight + [int(weight)]
        db.session.commit()

    def get_exercise_weight(self, exercise_id: int):
        """Get the weight of a specific exercise

        :param exercise_id: integer id of the exercise
        :return: exercise adjusted for weight
        """
        exercise_id = int(exercise_id)
        # if our weight arrays haven't been instantiated, instantiate them
        # prevents "None Type is non-iterable" error.
        if self.exercise_weight_id is None:
            self.exercise_weight_id = []
            self.exercise_weight = []
            db.session.commit()
        # if we've selected a custom weight, return that weight
        if exercise_id in self.exercise_weight_id:
            i = self.exercise_weight_id.index(exercise_id)
            return self.exercise_weight[i]
        # if we haven't customized the weight, return the default weight
        # based on bmi
        else:
            return exerciseplan.get_weight(
                exercise_id,
                self.height,
                self.weight
            )

    def set_exercise(self, exercise_id: int) -> None:
        """Set current exercise for the current user.

        :param exercise_id: integer id of exercise
        """
        self.current_exercise_id = exercise_id
        db.session.commit()

    def get_exercise_weights(self) -> List:
        """Get a list of all exercise weights.

        :return:
        """
        weights = []
        for e in exerciseplan.get_w_exercises():
            weights.append([id, self.get_exercise_weight(e.getid())])

        return weights

    def get_exercise(self) -> int:
        """Get current exercise.

        Handles case where you haven't selected an exercise as well.

        :return: integer id of current exercise
        """
        if self.current_exercise_id is None:
            return -1

        return self.current_exercise_id

    def set_mealplan(self, plan_id: int) -> None:
        """Set current mealplan.

        :param plan_id: integer id of mealplan
        """
        self.current_mealplan_id = plan_id
        db.session.commit()

    def get_mealplan(self) -> int:
        """Get current mealplan.

        Handles case where you haven't selected a mealplan as well.

        :return: integer id of mealplan
        """
        if self.current_mealplan_id is None:
            return -1

        return self.current_mealplan_id

    def url_for(self):
        """Returns the url stub for the current user.

        :return: url stub for current user
        """
        return f'/user/{self.username}'

    def post_count(self) -> int:
        """Returns the number of posts authored by the current user.

        :return: integer number of posts
        """
        return len(list(self.posts))


# vim: ft=python ts=4 sw=4 sts=4 et
