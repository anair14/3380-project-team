from . import db


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)


# vim: ft=python ts=4 sw=4 sts=4 et
