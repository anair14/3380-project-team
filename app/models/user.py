from datetime import date
from multiprocessing.dummy import Array
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .exercise import ExercisePlan
from .meal import MealPlan

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
        return f'<User {self.username}>'

    def set_password(self, new_password: str) -> None:
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

    def list_followers(self, user):
        return self.follower.count()

    def set_exercise_weight(self, exercise_id, weight):
        self.exercise_weight_id.append(exercise_id)
        self.exercise_weight.append(weight)

    def get_exercise_weight(self,exercise_id):
        i = self.exercise_weight_id.index(exercise_id)
        return self.exercise_weight[i]   

# vim: ft=python ts=4 sw=4 sts=4 et
