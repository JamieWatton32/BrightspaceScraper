# Requirements:
# Selenium: https://pypi.org/project/selenium/ pip install selenium
# Numpy: https://pypi.org/project/numpy/ pip install numpy
# Pandas: https://pypi.org/project/pandas/ pip install pandas
#Beautifulsoup4: https://pypi.org/project/beautifulsoup4/ pip install bs4

#-------------------------------------------------------------

# This sets up the webdriver. This only works in firefox HOWEVER you can use chrome using this instead: 
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)
# **note that I havent tested it in chrome. not all web drivers are the same so your milage may vary.
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
def Scraper():
    #Use this for firefox
    options = Options()
    #options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)



    #Use this for chrome
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(options=options)


    #0----------------------------------------------
    # This here sets up the base url of brightspace "https://schoolspecific.brightspace.com" is the typical url base.
    # It also sets up the various buttons that need to be clicked though to get through MSFT login. 
    # the getPass import is a input that is passed to your password variable in order to keep it out of the source. 

    import getpass # so you don't show your password in the sourcecode
    email = input("Enter your Email")
    base_url = 'https://nscconline.brightspace.com'
    password = getpass.getpass()
    email_field = (By.ID, 'i0116')
    password_field = (By.ID, 'i0118')
    next_button = (By.ID, 'idSIButton9')

    #This just runs through the MSFT login process inorder to get to the brightspace homepage
    driver.get(base_url)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable(email_field)).send_keys(email)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable(next_button)).click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable(password_field)).send_keys(password)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable(next_button)).click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable(next_button)).click()

    # This block Iterates through a list of validated grade page urls. 
    # on each page the page source is parsed using beautifulsoup4. (Much faster than selenium btw!)
    # The parsed html then is put into a list of dataframes (df=[]) then empty columns get popped.

    grades_extensions = ["/d2l/lms/grades/my_grades/main.d2l?ou=299885",
                        "/d2l/lms/grades/my_grades/main.d2l?ou=297335",
                        "/d2l/lms/grades/my_grades/main.d2l?ou=295501",
                        "/d2l/lms/grades/my_grades/main.d2l?ou=295683",
                        "/d2l/lms/grades/my_grades/main.d2l?ou=297213"
                        ]
    from datetime import datetime

    #Extensions for the wuiz windows of OSYS. This is only needed since he doesn't put them into the grades window.
    windows_quiz_extensions = ['/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324825&ou=295501',#quiz 1 
                            '/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324827&ou=295501',#quiz 2
                            '/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324826&ou=295501',#quiz 3
                            '/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324828&ou=295501',#quiz 4
                            '/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324832&ou=295501',#quiz 5
                            '/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324830&ou=295501',#quiz 6
                            '/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324829&ou=295501',#quiz 7
                            ]

    if datetime.now() > datetime(2024,3,3,23,30):
        windows_quiz_extensions.append('/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324831&ou=295501')#quiz 8
    elif datetime.now() > datetime(2024,4,7,23,30):
        windows_quiz_extensions.append('/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324833&ou=295501')#quiz 9
    elif datetime.now() > datetime(2024,4,14,23,30):
        windows_quiz_extensions.append('/d2l/lms/quizzing/user/quiz_submissions.d2l?qi=324834&ou=295501')#quiz 10

    import pandas as pd
    import io
    import os
    from bs4 import BeautifulSoup as bs4
    url = []
    df = []
    new_df=[]
    #Iterates through list of grade page urls. Nested loop then extracts the <table> contents from the HTML on each page
    for each in grades_extensions:
        url = base_url + each
        driver.get(url)
        soup = bs4(driver.page_source, 'html.parser')
        soup = io.StringIO(str(soup))
        df = pd.read_html(soup)

    
        #This clears out the columns "Points" and "Comments and Assessments". 
        for i in df:
            i.pop("Points")
            i.pop("Comments and Assessments")
            new_df.append(i)
            
    for each in windows_quiz_extensions:
        url = base_url + each
        driver.get(url)
        soup = bs4(driver.page_source, 'html.parser')
        soup = io.StringIO(str(soup))
        df = pd.read_html(soup)
        for i in df:
            new_df.append(i)

    #Here the cleaned dataframes are broken up and are written to a csv respectively.This doesn't have to be done
    #but this file is getting long and reading a csv for each class in another .py file 
    #is easier than debugging a 100+ line file.  
    csv_file_folder = "./CsvFiles"
    os.mkdir(csv_file_folder)
    #Networking
    new_df[0].to_csv("./CsvFiles/Networking.csv",index=False)

    #DATA FUND
    new_df[1].to_csv("./CsvFiles/DataFund.csv",index=False)

    #OSYS
    new_df[2].to_csv("./CsvFiles/Osys.csv",index=False)

    #WEBDEV
    new_df[3].to_csv("./CsvFiles/Webdev.csv",index=False)

    #Programming  
    new_df[4].to_csv("./CsvFiles/Prog.csv",index=False)

    #Osys quiz 1
    new_df[5].to_csv("./CsvFiles/OsysQuiz1.csv",index=False)

    #Osys quiz 2
    new_df[6].to_csv("./CsvFiles/OsysQuiz2.csv",index=False)

    #Osys quiz 3
    new_df[7].to_csv("./CsvFiles/OsysQuiz3.csv",index=False)

    #Osys quiz 4
    new_df[8].to_csv("./CsvFiles/OsysQuiz4.csv",index=False)

    #Osys quiz 5
    new_df[9].to_csv("./CsvFiles/OsysQuiz5.csv",index=False)

    #Osys quiz 6
    new_df[10].to_csv("./CsvFiles/OsysQuiz6.csv",index=False)

    #Osys quiz 7
    new_df[11].to_csv("./CsvFiles/OsysQuiz7.csv",index=False)

    if datetime.now() > datetime(2024,3,3,23,30):
        #Osys quiz 8
        new_df[12].to_csv("./CsvFiles/OsysQuiz8.csv",index=False)

    elif datetime.now() > datetime(2024,4,7,23,30):
        #Osys quiz 9
        new_df[13].to_csv("./CsvFiles/OsysQuiz9.csv",index=False)

    elif datetime.now() > datetime(2024,4,14,23,30):
        #Osys quiz 10
        new_df[14].to_csv("./CsvFiles/OsysQuiz10.csv",index=False)
    driver.close()

if __name__ == "__main__":
    Scraper()