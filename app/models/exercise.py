from .import db


class ExercisePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    reps = db.Column(db.Integer, index=True, unique=False)
    sets = db.Column(db.Integer, index=True, unique=False)


# class ExercisePlan(db.Model):
#     id = db.Column(db.Integer, primary_key=True)


# vim: ft=python ts=4 sw=4 sts=4 et
