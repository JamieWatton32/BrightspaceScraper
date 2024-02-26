#This file is responsible for the calculations from the written csv files. 
#if the crawler hasn't been ran yet it will find it based on if the existance of ./CsvFiles returns true
from datetime import datetime
import numpy as np
import pandas as pd
import os

if os.path.isdir("./CsvFiles") == False:
    import Scraper

#Storing each file path as a string to help with readability
networking_file = "./CsvFiles/Networking.csv"
osys_file = "./CsvFiles/Osys.csv"
datafund_file = "./CsvFiles/DataFund.csv"
web_file = "./CsvFiles/Webdev.csv"
prog_file = "./CsvFiles/Prog.csv"
df0 = pd.read_csv(networking_file)#Networking
df1 = pd.read_csv(osys_file)#Osys
df2 = pd.read_csv(datafund_file)#Data fundamentals
df3= pd.read_csv(web_file)#Web development
df4 = pd.read_csv(prog_file)#Programming


#This function  
def osys_quiz() -> float:
    osys_quizzies =[pd.read_csv('./CsvFiles/OsysQuiz1.csv').to_numpy(),
                    pd.read_csv('./CsvFiles/OsysQuiz2.csv').to_numpy(),
                    pd.read_csv('./CsvFiles/OsysQuiz3.csv').to_numpy(),
                    pd.read_csv('./CsvFiles/OsysQuiz4.csv').to_numpy(),
                    pd.read_csv('./CsvFiles/OsysQuiz5.csv').to_numpy(),
                    pd.read_csv('./CsvFiles/OsysQuiz6.csv').to_numpy(),
                    pd.read_csv('./CsvFiles/OsysQuiz7.csv').to_numpy(),
                    ]
    if datetime.now() > datetime(2024,3,3,23,30):
        osys_quizzies.append(pd.read_csv("./CsvFiles/OsysQuiz8.csv").to_numpy()) 

    elif datetime.now() > datetime(2024,4,7,23,30):
        osys_quizzies.append(pd.read_csv('./CsvFiles/OsysQuiz9.csv').to_numpy())

    elif datetime.now() > datetime(2024,4,14,23,30):
        osys_quizzies.append(pd.read_csv('./CsvFiles/OsysQuiz10.csv').to_numpy())
    grades = []
    total=int(0)

    for i in osys_quizzies:
        if i[-1][0] == 'Overall Grade (highest attempt):':
            grades.append(float(i[-1][1])/50)
    for j in grades:
        total += j
    return total

def osys_grades() -> float:
    #these 3 lines are dropping empty rows, dropping duplicate rows, 
    #and converting it to a NumPy array for processing
    df1.dropna()
    df1.drop_duplicates()
    df_osys = df1.to_numpy()
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
        "Quizzies":osys_quiz(),
        "Final Project":float(current[2])
        }
    Actual = 0
    Actual = current_grade['Assignments'] + current_grade["Final Project"] +current_grade["Quizzies"] 
    print(f'Your current grade in OSYS is {Actual}%')
#put stuff here           
def Networking():
    df_netw = df0.to_numpy()
    netw_dict = {}
    grades = []
    current_grade_before = []
    current_total=[]
    assign_current = []
    quiz_current = []
    midterm_current = []
    final_current =[]
    assign_poss = []
    quiz_poss = []
    midterm_poss=[]
    final_poss=[]

   
    for i in df_netw:
        if i[1] == "Weekly Assignments":# or i[1] != 'Weekly Quizzes': or i[1] !='Midterm Test' or i[1] !='Final Exam':
            continue
        elif i[1] == 'Weekly Quizzes':
            continue
        elif i[1] =='Midterm Test':
            continue
        elif i[1] =='Final Exam':
            continue
        else:
            grades.append((i[2]).split('/'))
    del grades[-1]        
    for each in grades:
        if each[0] == '- ':
           each[0] = 0
           each[1] = 0
        current_grade_before.append(float(each[0]))
        current_total.append(float(each[1]))

    
    count = 0
    for i in current_grade_before:
        if count <= 5:
            assign_current.append(i)
        elif count > 5 and count <=11:
            quiz_current.append(i)
        elif count == 12:
            midterm_current.append(i)
        elif count == 13:
            final_current.append(i)
        count +=1
    count = 0
    for i in current_total:
        if count <= 5:
            assign_poss.append(i)
        elif count > 5 and count <=11:
            quiz_poss.append(i)
        elif count == 12:
            midterm_poss.append(i)
        elif count == 13:
            final_poss.append(i)
        count +=1
    
    assign_worth_each = 8
    actual_grades = []
    count=0
    for i in assign_current:
        try:
            i = assign_worth_each*i/assign_poss[count]
            actual_grades.append(i)
        except ZeroDivisionError:
            actual_grades.append(0)
        count+=1
    
    
    count=0
    quiz_worth_each = 2
    for i in quiz_current:
        try:
            i = quiz_worth_each*i/assign_poss[count]
            actual_grades.append(i)
        except ZeroDivisionError:
            actual_grades.append(0) 
    actual_grades.append(midterm_current[0])
    actual_grades.append(final_current[0])
    total = 0
    for i in actual_grades:
        total +=i
    total = total 
    print(f'Your current grade in networking is: {total:.2f}%')
    
#put stuff here 
def data_fundamentals():
    pass
#put stuff here 
def web_dev():
    pass
#put stuff here 
def prog_logic():
    pass

def main():
    osys_grades()
    Networking()
    #Removes files off your system if yes
    delete_files = input("Delete csv files?(y/n) ").lower()
    if delete_files == "y":
        os.remove("./CsvFiles/Networking.csv")
        os.remove("./CsvFiles/Osys.csv")
        os.remove("./CsvFiles/DataFund.csv")
        os.remove("./CsvFiles/Webdev.csv")
        os.remove("./CsvFiles/Prog.csv")
        os.remove("CsvFiles/OsysQuiz1.csv")
        os.remove("CsvFiles/OsysQuiz2.csv")
        os.remove("CsvFiles/OsysQuiz3.csv")
        os.remove("CsvFiles/OsysQuiz4.csv")
        os.remove("CsvFiles/OsysQuiz5.csv")
        os.remove("CsvFiles/OsysQuiz6.csv")
        os.remove("CsvFiles/OsysQuiz7.csv")
        if datetime.now() > datetime(2024,3,3,23,30):
            os.remove("./CsvFiles/OsysQuiz8.csv")

        elif datetime.now() > datetime(2024,4,7,23,30):
            os.remove("./CsvFiles/OsysQuiz9.csv")

        elif datetime.now() > datetime(2024,4,14,23,30):
            os.remove("./CsvFiles/OsysQuiz10.csv")
        os.removedirs('./CsvFiles')

if __name__ =="__main__":
        main()
