from re import I
from flask import Flask
import json
from pathlib import Path


class Exercise():
    def __init__(self, id, name, calories, diff, type, region, part, sets, reps, weighted):
        self.id = id
        self.name = name
        self.calories = calories
        self.diff = diff
        self.type = type
        self.region = region
        self.part = part
        self.sets = sets
        self.reps = reps
        self.weighted = True
        if(region == 'arms'):
            self.weight_light = 20
            self.weight_medium = 30
            self.weight_heavy = 40
        elif(region == 'legs'):
            self.weight_light = 50
            self.weight_medium = 70
            self.weight_heavy = 90



    def getweight(self, bmi):
        if self.weighted:
            if bmi < 18.5:
                return self.weight_light
            elif bmi < 24.9:
                return self.weight_medium
            else:
                return self.weight_heavy
        else:
            return None

    def isweighted(self):
        return self.weighted

    def getid(self):
        return self.id

    def __str__(self):
        return self.name

def getexercises():
    return exercises_weighted + exercisesn_weighted

def getwexercises():
    return exercises_weighted
        

    
def getexercise(id: int):
    # print("here1")
    id = int(id)
    for exercise in exercises_weighted:
        if exercise.id == id:
            return exercise
    for exercise in exercisesn_weighted:
        if exercise.id == id:
            return exercise
    return None

def getexercise_basedonname(name):
    for exercise in exercises_weighted:
        if exercise.name == name:
            return exercise
    for exercise in exercisesn_weighted:
        if exercise.name == name:
            return exercise
    return None

def getweight(id, height, weight):
    bmi = weight/height
    e = getexercise(id)
    return e.getweight(bmi)
    

exercises_weighted = []
exercisesn_weighted = []
p = Path(Path.cwd(), 'app', 'json_info', 'exercise_file.json')
print(p)
f = open(p, "r")
data = json.load(f)
i = 0
#exercisesn_weighted.append(Exercise(-1, 'N/A', 0, 0, 0, 0, 0, 0, 0, True))
for e in data:
#    exercises.append(i, e['name'], e['calories'], e['difficulty'], e['type'], e['region'], e['specific body part'], e['sets'], e['reps'])
    # exercises.append(i, e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7])
    ex = data[e]
    if(data[e]['weights'] == "no"):
        exercisesn_weighted.append(Exercise(i, data[e]['name'], data[e]['calories'], data[e]['difficulty'], 
                    data[e]['type'], data[e]['region'], data[e]['specific body part'], data[e]['sets'], 
                    data[e] ['reps'], False))
    else:
        exercises_weighted.append(Exercise(i, data[e]['name'], data[e]['calories'], data[e]['difficulty'], 
                data[e]['type'], data[e]['region'], data[e]['specific body part'], data[e]['sets'], 
                data[e] ['reps'], True))
    i = i+1


    
