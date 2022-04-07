from re import I
from flask import Flask
import json
from pathlib import Path


#class to represent exercises
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
        self.weighted = weighted
        #default weights based upon which region it targets
        if(region == 'arms'):
            self.weight_light = 20
            self.weight_medium = 30
            self.weight_heavy = 40
        elif(region == 'legs'):
            self.weight_light = 50
            self.weight_medium = 70
            self.weight_heavy = 90


    #get the weight for an exercise based on a user's bmi
    def get_weight(self, bmi):
        if self.weighted:
            if bmi < 18.5:
                return self.weight_light
            elif bmi < 24.9:
                return self.weight_medium
            else:
                return self.weight_heavy
        else:
            return None

    #return whether or not an exercise requires weights
    def is_weighted(self):
        return self.weighted

    #get weight id
    def get_id(self):
        return self.id

    #string version of exercise
    def __str__(self):
        return self.name
        
class ExercisePlan():
    def __init__(self):
        #load exercises from exercise_file.json
        #two separate lists for weighted vs nonweighted exercises
        self.exercises_weighted = []
        self.exercisesn_weighted = []
        p = Path(Path.cwd(), 'app', 'json_info', 'exercise_file.json')
        f = open(p, "r")
        data = json.load(f)
        i = 0
        self.exercisesn_weighted.append(Exercise(-1, 'No Exercise Selected Yet', 0, 0, 0, 0, 0, 0, 0, True))
        for e in data:
            #if not weighted, add to exercisesn_weighted with weighted = False
            if(data[e]['weights'] == "no"):
                self.exercisesn_weighted.append(Exercise(i, data[e]['name'], data[e]['calories'], data[e]['difficulty'], 
                            data[e]['type'], data[e]['region'], data[e]['specific body part'], data[e]['sets'], 
                            data[e] ['reps'], False))
            #if weighted, add to exercises_weighted with weighted = True
            else:
                self.exercises_weighted.append(Exercise(i, data[e]['name'], data[e]['calories'], data[e]['difficulty'], 
                        data[e]['type'], data[e]['region'], data[e]['specific body part'], data[e]['sets'], 
                        data[e] ['reps'], True))
            i = i+1

    #get all exercises
    def get_exercises(self):
        #ensure the blank exercise doesn't get used
        return self.exercises_weighted + self.exercisesn_weighted[1:]

    #get weighted exercises
    def get_w_exercises(self):
        return self.exercises_weighted
            

    #get specific exercise based off id   
    def get_exercise(self, id: int):
        id = int(id)
        #run through both weighted and unweighted exercises
        for exercise in self.exercises_weighted:
            if exercise.id == id:
                return exercise
        for exercise in self.exercisesn_weighted:
            if exercise.id == id:
                return exercise
        #return None if not found
        return None

    #get specific exercise baed off id
    def get_exercise_based_on_name(self, name):
        for exercise in self.exercises_weighted:
            if exercise.name == name:
                return exercise
        for exercise in self.exercisesn_weighted:
            if exercise.name == name:
                return exercise
        return None

    #get a specific exercises weight based on it's id, 
    #and the users personal info
    def get_weight(self, id, height, weight):
        bmi = weight/height
        e = self.get_exercise(id)
        return e.get_weight(bmi)
        



    
