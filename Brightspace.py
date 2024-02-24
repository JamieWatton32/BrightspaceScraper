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

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
options.add_argument("-headless")
options.add_argument('--no-sandbox')

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


#Here the cleaned dataframes are broken up and are written to a csv respectively.This doesn't have to be done
#but this file is getting long and reading a csv for each class in another .py file 
#is easier than debugging a 100+ line file.  
df0 = new_df[0]
df1 = new_df[1]
df2 = new_df[2]
df3 = new_df[3]
df4 = new_df[4]
#TODO: REMOVE THIS TRY-EXCEPT BEFORE FINAL COMMIT. 
csv_file_folder = "./CsvFiles/"
try:
    os.mkdir(csv_file_folder)
    
    #Networking
    df0 = new_df[0]
    df0.to_csv("./CsvFiles/Networking.csv",index=False)

    #DATA FUND
    df1 = new_df[1]
    df1.to_csv("./CsvFiles/DataFund.csv",index=False)


    #OSYS
    df2 = new_df[2]#OSYS 
    df2.to_csv("./CsvFiles/Osys.csv",index=False)

    #WEBDEV
    df3 = new_df[3]#
    df3.to_csv("./CsvFiles/Webdev.csv",index=False)

    #Programming  
    df4 = new_df[4]
    df4.to_csv("./CsvFiles/Prog.csv",index=False)

    #Concatenating all dataframes to a csv file. Not super needed but helps to view the data. 
    print(f'./CsvFiles/parent.csv already exists. Moving on...')
    pd.concat([df0,df1,df2,df3,df4], axis=1).to_csv("./CsvFiles/parent.csv", index=False)
except FileExistsError:
    print(f'Exiting..')
   