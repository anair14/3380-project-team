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
from ..json_info import load_exercise
from ..json_info import load_mealplans

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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150),
                         index=True,
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(150), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_completed = db.Column(db.Boolean(), default=False, nullable=False)

    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    birthdate = db.Column(db.Date())
    height = db.Column(db.Float())
    weight = db.Column(db.Float())
    current_exercise_id = db.Column(db.Integer())
    exercise_weight_id = db.Column(db.PickleType())
    exercise_weight = db.Column(db.PickleType())
    current_mealplan_id = db.Column(db.Integer())
    # display_metric = db.Boolean

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
        return f'<User {self.username}, id: {self.id}, current_exercise_id {self.current_exercise_id}, exercise_weight_id {self.exercise_weight_id}>'

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

    def set_exercise_weight(self, exercise_id, weight):
        if self.exercise_weight_id is None:
            self.exercise_weight_id = [exercise_id]
            self.exercise_weight = [weight]
        else:
            self.exercise_weight_id = self.exercise_weight_id.append(exercise_id)
            self.exercise_weight.append(weight)
        db.session.commit()

    def get_exercise_weight(self, exercise_id):
        print(self)
        if(self.exercise_weight_id is None):
            self.exercise_weight_id = []
            self.exercise_weight = []
            db.session.commit()
        if(exercise_id in self.exercise_weight_id):
            i = self.exercise_weight_id.index(exercise_id)
            return self.exercise_weight[i]
        else:
            return load_exercise.getweight(exercise_id, self.height, self.weight)

    def setexercise(self, exercise_id):
        print(exercise_id)
        self.current_exercise_id = exercise_id
        db.session.commit()

    def get_exercise_weights(self):
        weights = []
        for e in load_exercise.getwexercises():
            weights.append([id, self.get_exercise_weight(e.getid())])
        return weights

    def get_exercise(self):
        if self.current_exercise_id is None:
            return -1
        return self.current_exercise_id

    def set_mealplan(self, id):
        self.current_mealplan_id = id
        db.session.commit()

    def get_mealplan(self):
        if self.current_mealplan_id is None:
            return -1
        return self.current_mealplan_id

    def url_for(self):
        return f'/user/{self.username}'

# vim: ft=python ts=4 sw=4 sts=4 et
