from . import db


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class ExercisePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)


# vim: ft=python ts=4 sw=4 sts=4 et
