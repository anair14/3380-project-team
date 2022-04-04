from flask import Flask
from flask_login import current_user
import json
from pathlib import Path


exercises = []
p = Path.cwd() / 'app\\json_info\\exercise_file.json'
print(p)
f = open(p, "r")
#data = json.load(f)

def Exercise():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def getweight(self, bmi):
        if bmi < 1:
            return self.weight_light
        elif bmi < 2:
            return self.weight_medium
        elif bmi < 3:
            return self.weight_heavy
    def __str__(self):
        return self.name

def getexercise(self, id):
    for exercise in exercises:
        if exercise.id == id:
            return exercise
    return None

def getweight(self, id, height, weight):
    bmi = weight/height
    e = getexercise(id)
    return e.getweight(bmi)
    
    
