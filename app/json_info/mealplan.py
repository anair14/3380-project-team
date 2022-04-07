from flask import Flask
from flask_login import current_user
import json
from pathlib import Path


#class to represent MealPlans
class Meal():
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

class MealPlan():
    def __init__(self):
        #load mealplans from mealplan_file.json
        self.mealplans_v = []
        self.mealplans = []
        p = Path(Path.cwd(), 'app', 'json_info', 'mealplan_file.json')
        f = open(p, "r")
        data = json.load(f)
        i = 0
        #append a mealplan for when you haven't selected one yet
        self.mealplans_v.append(Meal(-1, "No Meal Selected Yet", 0, 0, True))
        for e in data:
            #if vegetarian, append to mealplans_v with vegetarian = True
            if data[e]['vegetarian'] == 'yes':
                self.mealplans_v.append(Meal(i, data[e]['name'], data[e]['calories'], data[e]['image'], True))
            #if not vegetarian, append to mealplans with vegetarian = False
            else:
                self.mealplans.append(Meal(i, data[e]['name'], data[e]['calories'], data[e]['image'], False))
            i = i+ 1

    #get specific mealplan with id
    def getmealplan(self, id):
        id = int(id)
        for mealplan in self.mealplans_v:
            if mealplan.id == id:
                return mealplan
        for mealplan in self.mealplans:
            if mealplan.id == id:
                return mealplan
        return None

    #get specific mealplan with name
    def getmealplan_basedonname(self, name):
        for mealplan in self.mealplans_v:
            if mealplan.name == name:
                return mealplan
        for mealplan in self.mealplans:
            if mealplan.name == name:
                return mealplan
        return None

    #get all mealplans
    def getmealplans(self):
        #ensure blank meal doesn't get used
        return self.mealplans + self.mealplans_v[1:]

    #get vegetarian mealplans
    def getmealplansv(self):
        return self.mealplans_v

    #get nonvegetarian mealplans
    def getmealplansnv(self):
        return self.mealplans


    
    
