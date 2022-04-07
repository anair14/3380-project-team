from flask import Flask
from flask_login import current_user
import json
from pathlib import Path


#class to represent MealPlans
class MealPlan():
    def __init__(self, id, name, calories, image_link, vegetarian):
        self.id = id
        self.name = name
        self.calories = calories
        self.image = image_link
        self.vegetarian = vegetarian

    #get calories
    def get_calories(self):
        return self.calories

    #get id of mealplan
    def getid(self):
        return self.id

    #string representation of mealplan
    def __str__(self):
        return self.name

#get specific mealplan with id
def getmealplan(id):
    id = int(id)
    for mealplan in mealplans_v:
        if mealplan.id == id:
            return mealplan
    for mealplan in mealplans:
        if mealplan.id == id:
            return mealplan
    return None

#get specific mealplan with name
def getmealplan_basedonname(name):
    for mealplan in mealplans_v:
        if mealplan.name == name:
            return mealplan
    for mealplan in mealplans:
        if mealplan.name == name:
            return mealplan
    return None

#get all mealplans
def getmealplans():
    #ensure blank meal doesn't get used
    return mealplans + mealplans_v[1:]

#get vegetarian mealplans
def getmealplansv():
    return mealplans_v

#get nonvegetarian mealplans
def getmealplansnv():
    return mealplans

#load mealplans from mealplan_file.json
mealplans_v = []
mealplans = []
p = Path(Path.cwd(), 'app', 'json_info', 'mealplan_file.json')
f = open(p, "r")
data = json.load(f)
i = 0
#append a mealplan for when you haven't selected one yet
mealplans_v.append(MealPlan(-1, "No Meal Selected Yet", 0, 0, True))
for e in data:
    #if vegetarian, append to mealplans_v with vegetarian = True
    if data[e]['vegetarian'] == 'yes':
        mealplans_v.append(MealPlan(i, data[e]['name'], data[e]['calories'], data[e]['image'], True))
    #if not vegetarian, append to mealplans with vegetarian = False
    else:
        mealplans.append(MealPlan(i, data[e]['name'], data[e]['calories'], data[e]['image'], False))
    i = i+ 1
    
    
