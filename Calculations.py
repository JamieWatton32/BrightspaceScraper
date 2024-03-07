#This file is responsible for the calculations from the written csv files. 
#if the crawler hasn't been ran yet it will find it based on if the existance of ./CsvFiles returns true
from datetime import datetime
import numpy as np
import pandas as pd
import os
from Scraper import Scraper

if os.path.isdir("./CsvFiles") == False:
    Scraper()

#Storing each file path as a string to help with readability
networking_file = "./CsvFiles/Networking.csv"
osys_file = "./CsvFiles/Osys.csv"
datafund_file = "./CsvFiles/DataFund.csv"
web_file = "./CsvFiles/Webdev.csv"
prog_file = "./CsvFiles/Prog.csv"




#This function calculates the total contribution of the quiz grades for OSYS 
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
    grades = [grades.append(float(each[-1][1])/50) for each in osys_quizzies if each[-1][0] == ['Overall Grade (highest attempt):']]
    total_grade = sum(grades)
    return total_grade

def osys_grades() -> float:
    df1 = pd.read_csv(osys_file)#Osys
    df_osys = df1.to_numpy()
    #for osys he enters the stuff including the zero so no linear interpolation is needed. 
    current = [i[2].split('/')[0] for i in df_osys if i[0] in ["Assignments", "Quizes", "Final Project"]]
    current_grade = [float(current[0]), osys_quiz(), float(current[2])]
    
    return current_grade[0] +current_grade[1]+ current_grade[2]


#data fundamentals grades
def data_fundamentals()-> float:
    df2 = pd.read_csv(datafund_file)#Data fundamentals
    df_data = df2.to_numpy()
    grades = [each[2].split('/')[0] for each in df_data if each[1] in ["Assignments","Quizzes", "In-Class Activities",'Tech Checks']]    
    return sum(float(grade) for grade in grades)
   
#web dev grades
def web_dev()-> float:
    df3= pd.read_csv(web_file)#Web development
    df_web = df3.to_numpy()
    grades = [each[2].split('/')[0] for each in df_web if each[1] in ["Assignments","Practicals","Final Project","Quizzes"]]
    return sum(float(grade) for grade in grades)
    
#programming grades 
def prog_logic()-> float:
    df4 = pd.read_csv(prog_file)#Programming 
    df_prog = df4.to_numpy()
    grades = [each[2].split('/')[0] for each in df_prog if each[1] in ["Assignments", "Tech Checks", "Final Project", "Quizzes (in-class exercises)"]]
    return sum(float(grade) for grade in grades)


#This function takes the networking array and scales grade interpolates the grades to a static scale that doesn't change as he grades stuff
#instead of it having the weird dyanmically updating scale that brightspace is doing        
def Networking() -> float:
    df0 = pd.read_csv(networking_file)#Networking
    df_netw = df0.to_numpy()
    
    assign_quiz_poss = []
    #This cleans out the rows that cannot be interpolated and extracts the ones that can into their own list. 
    grades = []
    for col in df_netw:
        if col[1] not in ['Weekly Assignments', 'Weekly Quizzes', 'Midterm Test']:
            grades.append((col[2]).split('/'))

    del grades[-1]#Just deleting the "bonus grade" on the bottom.     

    #This turns separates the received mark and the possible mark for each item. 
    #If the item is empty then the "-" is converted to 0 in order to add it to the total 
    current_grade_before = []
    current_total=[]
    for each in grades:
        if each[0] == '- ':
           each[0] = 0
           each[1] = 0
        current_grade_before.append(float(each[0]))
        current_total.append(float(each[1]))

    midterm_current = current_grade_before[12]#setting midterm grade since the list will be broken up later
    final_current=current_grade_before[13]#setting final grade since the list will be broken up later

    count = 0
    assign_current = []
    quiz_current = []
    for i in current_grade_before:
        if count <= 5:
            assign_current.append(i)
        elif  count <=11:
            quiz_current.append(i)
        count +=1
    assign_quiz_poss = []
    #This creates a possible list for assignment grades
    for count in range(0,11):
        assign_quiz_poss.append(current_total[count])
    

    #This block does the interpolation of the assignment and quizzes from the dyanmic scale to the static scale.
    assign_worth_each = 8
    actual_grades = []
    count=0
    for grade in assign_current:
        try:
            grade = assign_worth_each*grade/assign_quiz_poss[count]
            actual_grades.append(grade)
        except ZeroDivisionError:
            continue
        count+=1
    
    count=0
    quiz_worth_each = 2
    for grade in quiz_current:
        try:
            grade = quiz_worth_each*grade/assign_quiz_poss[count]
            actual_grades.append(grade)
        except ZeroDivisionError:
            continue
        count+=1

    #returns your Networking grade. 
    return sum(actual_grades) + midterm_current +final_current  
   

def main():
    print(f'Your current grades, assuming 0 in everything going forward is:\n')
    print(f'Your current grade in OSYS is {osys_grades():.2f}%')
    print(f'Your current grade in networking is: {Networking():.2f}%')
    print(f'Your current grade in data fundamentals is: {data_fundamentals():.2f}%')
    print(f'Your current grade in Web development is: {web_dev():.2f}%')
    print(f'Your current grade in programming and logic is: {prog_logic():.2f}%')
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
