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
url = []
df = []
cleaned_df=[]
#Iterates through list of grade page urls. Nested loop then extracts the <table> contents from the HTML on each page
for each in grades_extensions:
    url = base_url + each
    driver.get(url)
    
    for x in url:
        tbl = io.StringIO(driver.find_element(By.CSS_SELECTOR,".d2l-grid-wrapper").get_attribute('outerHTML'))
        df  = pd.read_html(tbl)
    #This clears out the columns "Points" and "Comments and Assessments". 
    for i in df:
        cleaned_df = i
        cleaned_df.pop("Points")
        cleaned_df.pop("Comments and Assessments")

       
        
