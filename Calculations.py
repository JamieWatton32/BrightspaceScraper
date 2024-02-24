#This file is responsible for the calculations from the written csv files. 
#if the crawler hasn't been ran yet it will find it based on if the existance of ./CsvFiles returns true

import numpy as np
import pandas as pd
import Brightspace
import os
if os.path.isdir("CsvFiles") == True:
    #Storing each file path as a string to help with readability
    networking_file = "./CsvFiles/Networking.csv"
    osys_file = "./CsvFiles/Osys.csv"
    datafund_file = "./CsvFiles/DataFund.csv"
    web_file = "./CsvFiles/Webdev.csv"
    prog_file = "./CsvFiles/Prog.csv"
    #Making dataframes out of the csv files (yes this is just the reverse of what I did in the other file but too bad)
    df0 = pd.read_csv(networking_file)#Networking
    df1 = pd.read_csv(osys_file)#Osys
    df2 = pd.read_csv(datafund_file)#Data fundamentals
    df3= pd.read_csv(web_file)#Web development
    df4 = pd.read_csv(prog_file)#Programming

    # Determines current grade in OSYS. 
    #TODO: SCRAPE QUIZ RESULTS NOW THAT BS4 IS MAKING IT FASTER
    def osys():

        #these 3 lines are dropping empty rows, dropping duplicate rows, 
        #and converting it to a NumPy array for processing
        df1.dropna()
        df1.drop_duplicates()
        df_osys = df1.to_numpy()
        #Empty lists for it. could probably be cleanmer but im bad at coding still so
        current = []
        total = []
        current_grade = {}
        
        #for osys he enters the stuff including the zero so no linear interpolation is needed. 
        for i in df_osys:
           if i[0] == "Assignments" or i[0] == "Quizes" or i[0] == "Final Project":
                current.append(i[2].split('/')[0])
                total.append(i[2].split('/')[1])
        #Making the current grades into a dictionary for betteris readability.    
        current_grade = {
            "Assignments":float(current[0]),
            "Quizzies":float(current[1]),
            "Final Project":float(current[2])
            }
        Actual = 0#This is redundant on a processing level but helps the f string from being 8 billion characters in length.
        Actual = current_grade['Assignments'] +current_grade["Final Project"] +current_grade["Quizzies"]
        print(f'Your current grade in OSYS is {Actual}, however your quiz grades have not been posted so take that into account. ')
    #put stuff here           
    def Networking():
        pass

    #put stuff here 
    def data_fundamentals():
        pass
    #put stuff here 
    def web_dev():
        pass
    #put stuff here 
    def prog_logic():
        pass
    #put stuff here     
    def main():
        osys()
    #calling main like usual.
    if __name__ =="__main__":
        main()
else:
    Brightspace