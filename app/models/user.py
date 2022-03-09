from . import db
from .exercise import ExercisePlan
from .meal import MealPlan
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), index=True, unique=True)
    email = db.Column(db.String(150), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    birthdate = db.Column(db.Date())
    height = db.Column(db.Float())
    weight = db.Column(db.Float())

    exercise_plan = ExercisePlan()
    meal_plan = MealPlan()

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, new_password: str) -> None:
        self.password_hash = generate_password_hash(new_password)

    def check_password_hash(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

# vim: ft=python ts=4 sw=4 sts=4 et
