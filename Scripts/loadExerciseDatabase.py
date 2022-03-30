import os, sys
p = os.path.abspath('.')
sys.path.insert(1, p)

from app import create_app
from flask import current_app, g
from app.models import db
import pandas as pd
from app.models.exercise import ExercisePlan


app = create_app('config.Development')
#app.run()

# db = g.db
with app.app_context():


    u = []
    df = pd.read_csv('Scripts/Exercises.csv')
    for row in df.iterrows():
        u.append(ExercisePlan(name = row[1][0], reps = row[1][2], sets = row[1][1]))
    for i in u:
        db.session.add(i)
    db.session.commit()