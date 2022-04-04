from re import I
from flask import Flask
from flask_login import current_user
import json
from pathlib import Path


class Exercise():
    def __init__(self, id, name, calories, diff, type, region, part, sets, reps):
        self.id = id
        self.name = name
        self.calories = calories
        self.diff = diff
        self.type = type
        self.region = region
        self.part = part
        self.sets = sets
        self.reps = reps


    def getweight(self, bmi):
        if bmi < 1:
            return self.weight_light
        elif bmi < 2:
            return self.weight_medium
        elif bmi < 3:
            return self.weight_heavy
    def __str__(self):
        return self.name

def getexercises():
    return exercises
    
def getexercise(id):
    for exercise in exercises:
        if exercise.id == id:
            return exercise
    return None

def getweight(id, height, weight):
    bmi = weight/height
    e = getexercise(id)
    return e.getweight(bmi)
    

exercises = []
p = Path(Path.cwd(), 'app', 'json_info', 'exercise_file.json')
print(p)
f = open(p, "r")
data = json.load(f)
i = 0
for e in data:
#    exercises.append(i, e['name'], e['calories'], e['difficulty'], e['type'], e['region'], e['specific body part'], e['sets'], e['reps'])
    # exercises.append(i, e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7])
    ex = data[e]
    exercises.append(Exercise(i, data[e]['name'], data[e]['calories'], data[e]['difficulty'], data[e]['type'], data[e]['region'], data[e]['specific body part'], data[e]['sets'], data[e] ['reps']))


    
