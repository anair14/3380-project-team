from flask import Flask
from flask_login import current_user
import json
from pathlib import Path


exercises = []
p = Path(Path.cwd(), 'app', 'json_info', 'mealplan_file.json')
print(p)
f = open(p, "r")
#data = json.load(f)

def MealPlan():
    def __init__(self, id, name):
        self.id = id
        self.name = name


def getmealplan(self, id):
    for exercise in exercises:
        if exercise.id == id:
            return exercise
    return None

    
    
