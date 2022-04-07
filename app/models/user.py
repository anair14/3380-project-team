from datetime import date
from flask import current_app as app
from multiprocessing.dummy import Array
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

from . import db
from .exercise import ExercisePlan
from .meal import MealPlan
from ..json_info import exercise
from ..json_info import mealplan

exerciseplan = exercise.ExercisePlan()

followers = db.Table(
    'followers',
    db.Column(
        'follower_id',
        db.Integer,
        db.ForeignKey('user.id')
    ),
    db.Column(
        'followed_id',
        db.Integer,
        db.ForeignKey('user.id')
    )
)

#class to represent a user
#most methods get called from current_user, meaning they effect the person currently signed in
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #login information
    username = db.Column(db.String(150),
                         index=True,
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(150), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_completed = db.Column(db.Boolean(), default=False, nullable=False)

    #personal information
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    birthdate = db.Column(db.Date())
    height = db.Column(db.Float())
    weight = db.Column(db.Float())
    current_exercise_id = db.Column(db.Integer())
    exercise_weight_id = db.Column(db.PickleType(), nullable = True)
    exercise_weight = db.Column(db.PickleType(), nullable = True)
    current_mealplan_id = db.Column(db.Integer())

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
    #string representation of user
    def __repr__(self):
        return f'<User {self.username}, id: {self.id}, current_exercise_id {self.current_exercise_id}, exercise_weight_id {self.exercise_weight_id}, exercise_weight {self.exercise_weight}>'

    def set_password(self, new_password: str) -> None:
        if app.debug:
            self.password_hash = generate_password_hash(new_password,
                                                        method='plain')
        else:
            self.password_hash = generate_password_hash(new_password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @hybrid_property
    def age(self):
        today = date.today()
        return ((today.year - self.birthdate.year)
                - ((today.month, today.day)
                   < (self.birthdate.month, self.birthdate.day)))

    @staticmethod
    def loader(user_id: int):
        return User.query.get(int(user_id))

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    #set an exercise weight to a custom value, rather than the default
    #user saves an array of all the exercise ids whose weights have changed
    #and another array that contains the actual weights of those exercises
    def set_exercise_weight(self, exercise_id, weight):
        #if array isn't initialized or empty 
        if self.exercise_weight_id is None or self.exercise_weight_id == []:
            self.exercise_weight_id = [exercise_id]
            self.exercise_weight = [weight]
        else:
            #if we've already changed the weight once want to simply modify our current weight array
            if exercise_id in self.exercise_weight_id:
                i = self.exercise_weight_id.index(exercise_id)
                #because db.pickletype saves a reference to the array, cannot simply use append
                #must create a new array through concatenation and pop the old elements out
                self.exercise_weight_id = self.exercise_weight_id + [exercise_id]
                self.exercise_weight = self.exercise_weight + [int(weight)]
                self.exercise_weight_id.pop(i)
                self.exercise_weight.pop(i)
            else:
                #because db.pickletype saves a reference to the array, cannot simply use append
                self.exercise_weight_id = self.exercise_weight_id + [exercise_id]
                self.exercise_weight = self.exercise_weight + [int(weight)]
        db.session.commit()

    #get the weight of a specific exercise
    def get_exercise_weight(self, exercise_id):
        exercise_id = int(exercise_id)
        #if our weight arrays haven't been instantiated, instantiate them
        #prevents "None Type is non-iterable" error.
        if(self.exercise_weight_id is None):
            self.exercise_weight_id = []
            self.exercise_weight = []
            db.session.commit()
        #if we've selected a custom weight, return that weight
        if(exercise_id in self.exercise_weight_id):
            i = self.exercise_weight_id.index(exercise_id)
            return self.exercise_weight[i]
        #if we haven't customized the weight, return the default weight based on bmi
        else:
            return exerciseplan.get_weight(exercise_id, self.height, self.weight)

    #set the users current exercise
    def set_exercise(self, exercise_id):
        self.current_exercise_id = exercise_id
        db.session.commit()

    #get a list of all exercise weights
    def get_exercise_weights(self):
        weights = []
        for e in exerciseplan.get_w_exercises():
            weights.append([id, self.get_exercise_weight(e.getid())])
        return weights

    #get current exercise, handles case where you haven't selected an exercise as well
    def get_exercise(self):
        if self.current_exercise_id is None:
            return -1
        return self.current_exercise_id

    #set current mealplan
    def set_mealplan(self, id):
        self.current_mealplan_id = id
        db.session.commit()

    #get current mealplan, handles case where you haven't selected a mealplan as well
    def get_mealplan(self):
        if self.current_mealplan_id is None:
            return -1
        return self.current_mealplan_id

    def url_for(self):
        return f'/user/{self.username}'

# vim: ft=python ts=4 sw=4 sts=4 et
