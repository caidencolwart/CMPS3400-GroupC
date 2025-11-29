import pickle
import os
import matplotlib as plt
import pandas as pd
import csv as csv
import numpy as np
from method_1 import DataVisualizer

#--------------Parent Class 2-----------------------------
#store data into data frame
#convert data frame to pickle file
#export pickle file and set up any output files directory
#put another objective here

class placeholderName:
    def __init__(self, filepath):
        self.filepath = filepath
        data = DataVisualizer(filepath)
        df = pd.read_csv(data.filepath)
        df.to_pickle('data.pkl')
        
        
#--------------Child Class 2-----------------------------
#Read the pickle file
#Probability
#Vectors
#Categorial Attribute Display

class dataCalculations(placeholderName):
    def __init__(self, __pklpath):
        self.__pklpath = __pklpath
        loaded_pkl = pickle.load(open(__pklpath, 'rb'))


    def calcProbabilities():
       x
    def calcVectors():
        x
    def catDisplay():
        x

