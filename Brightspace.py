from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
options.add_argument("-headless")
options.add_argument('--no-sandbox')


import getpass # so you don't show your password in the sourcecode
email = 'w0499673@campus.nscc.ca'
base_url = 'https://nscconline.brightspace.com'
password = getpass.getpass()
email_field = (By.ID, 'i0116')
password_field = (By.ID, 'i0118')
next_button = (By.ID, 'idSIButton9')

driver.get(base_url)
WebDriverWait(driver,10).until(EC.element_to_be_clickable(email_field)).send_keys(email)
WebDriverWait(driver,10).until(EC.element_to_be_clickable(next_button)).click()
WebDriverWait(driver,10).until(EC.element_to_be_clickable(password_field)).send_keys(password)
WebDriverWait(driver,10).until(EC.element_to_be_clickable(next_button)).click()
WebDriverWait(driver,10).until(EC.element_to_be_clickable(next_button)).click()
#                      Network                                      Osys
grades_extensions = ["/d2l/lms/grades/my_grades/main.d2l?ou=299885",
                     "/d2l/lms/grades/my_grades/main.d2l?ou=297335",
                     "/d2l/lms/grades/my_grades/main.d2l?ou=295501",
                     "/d2l/lms/grades/my_grades/main.d2l?ou=295683",
                     "/d2l/lms/grades/my_grades/main.d2l?ou=297213"
                    ]
import pandas as pd
import io
import os
url = []
df = []
new_df=[]
#Iterates through list of grade page urls. Nested loop then extracts the <table> contents from the HTML on each page
for each in grades_extensions:
    url = base_url + each
    driver.get(url)
    
    for x in url:
        tbl = io.StringIO(driver.find_element(By.CSS_SELECTOR,".d2l-grid-wrapper").get_attribute('outerHTML'))
        df  = pd.read_html(tbl)
    #This clears out the columns "Points" and "Comments and Assessments". 
    for i in df:
        i.pop("Points")
        i.pop("Comments and Assessments")
        new_df.append(i)
df0 = new_df[0]
df1 = new_df[1]
df2 = new_df[2]
df3 = new_df[3]
df4 = new_df[4]

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
    driver.close()