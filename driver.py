from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import os
from fetcher import fetch_errorlogs, fetch_generation_data
from database import commit_error_logs, initialize_db, commit_generation_logs
from login import login

''' configuring Selenium '''

chrome_driver_path = os.getcwd() + os.sep + 'chromedriver'
download_path = os.getcwd()

prefs = {
    "profile.default_content_settings.popups": 0,
    "download.default_directory": download_path,
    "directory_upgrade": True
}

''' end of configuration '''

def init_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)


with init_driver() as driver:
    login_url = "http://www.injectsolar.com/portal/#/login"
    errorlog_url = 'http://www.injectsolar.com/portal/#/inject-solar/errore-log'

    #login into the portal
    print("logging in..")
    login(driver,login_url)
    print("successfully logged in..")

    cursor, db = initialize_db()

    #fetch energy generated data
    gen_periods = [
        {'month': 'January', 'year': '2020'}, {'month': 'February','year': '2020'}
    ]
    for gen_period in gen_periods:
        _file_name = fetch_generation_data(driver,gen_period['month'],gen_period['year'], download_path)
        commit_generation_logs(cursor, db, _file_name)

    #fetch error logs
    err_periods = [
        {'start_date': '1/1/2020', 'end_date': '29/2/2020', 'alarm_type': 'Cleared Alarms'}
    ]
    for err_period in err_periods:
        _file_name = fetch_errorlogs(driver,err_period['start_date'],err_period['end_date'], err_period['alarm_type'], errorlog_url,download_path)
        commit_error_logs(cursor, db, _file_name)
    driver.quit()