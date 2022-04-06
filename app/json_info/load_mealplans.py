from flask import Flask
from flask_login import current_user
import json
from pathlib import Path


mealplans_v = []
mealplans = []
p = Path(Path.cwd(), 'app', 'json_info', 'mealplan_file.json')
print(p)
f = open(p, "r")
#data = json.load(f)

class MealPlan():
    def __init__(self, id, name, calories, image_link, vegetarian):
        self.id = id
        self.name = name
        self.calories = calories
        self.image = image_link
        self.vegetarian = vegetarian

    def get_calories(self):
        return self.calories

    def getid(self):
        return self.id

    def __str__(self):
        return self.name


def getmealplan(id):
    for mealplan in mealplans_v:
        if mealplan.id == id:
            return mealplan
    for mealplan in mealplans:
        if mealplan.id == id:
            return mealplan
    return None

def getmealplans():
    return mealplans + mealplans_v

def getmealplansv():
    return mealplans_v

def getmealplansnv():
    return mealplans

p = Path(Path.cwd(), 'app', 'json_info', 'mealplan_file.json')
#print(p)
f = open(p, "r")
data = json.load(f)
i = 0
for e in data:
    if data[e]['vegetarian'] == 'yes':
        mealplans_v.append(MealPlan(i, data[e]['name'], data[e]['calories'], data[e]['image'], True))
    else:
        mealplans.append(MealPlan(i, data[e]['name'], data[e]['calories'], data[e]['image'], False))
    i = i+ 1
    
    
