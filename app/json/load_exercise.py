from flask import Flask
from flask_login import current_user
import json

exercises = []
with open("exercise_file.json", "r") as read_file:
    data = json.load(read_file)

def Exercise():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name

def getexercise(self, id):
    for exercise in exercises:
        if exercise.id == id:
            return exercise
    return None
    
