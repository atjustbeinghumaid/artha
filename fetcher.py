import time
import os
import datetime


def fetch_generation_data(driver, month, year, dl_path):
    time.sleep(3)
    _day_ = driver.find_element_by_id('nav-profile-tab')
    driver.execute_script("arguments[0].click();", _day_)

    print("openning calendar...")
    time.sleep(3)
    calendar = driver.find_element_by_css_selector("button[aria-label='Open calendar']")
    driver.execute_script("arguments[0].click();",calendar)


    print("choosing year...")
    time.sleep(3)
    year_picker = driver.find_element_by_css_selector("td[aria-label = '{}']".format(year))
    driver.execute_script("arguments[0].click()", year_picker)


    print("choosing month...")
    time.sleep(3)
    month_picker = driver.find_element_by_css_selector("td[aria-label = '{}']".format(month + ' ' + year))
    driver.execute_script("arguments[0].click();", month_picker)


    print("clicking context menu...")
    time.sleep(5)
    driver.find_element_by_class_name("highcharts-exporting-group").click() 

    print("downloading xls file...")
    download = driver.find_element_by_xpath("//*[contains(text(), 'Download XLS')]")
    driver.execute_script("arguments[0].click();", download)
    time.sleep(5)
    downloaded_file_name = dl_path + os.sep + 'chart.xls'    
    new_file_name = dl_path + os.sep + month + '_' + year
    os.replace(downloaded_file_name, new_file_name)
    return new_file_name


def fetch_errorlogs(driver,start_date, end_date, log_type, errorlog_url, dl_path):

    driver.get(errorlog_url)

    clr_alarm = driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(log_type))
    driver.execute_script("arguments[0].click();", clr_alarm)

    start_date = start_date.split('/')
    end_date = end_date.split('/')
    start_date = datetime.datetime(int(start_date[2]), int(start_date[1]), int(start_date[0]))
    end_date = datetime.datetime(int(end_date[2]), int(end_date[1]), int(end_date[0]))
    
    calendars = driver.find_elements_by_css_selector("button[aria-label='Open calendar']")

    for i in range(len(calendars)):
        date = start_date if i == 0 else end_date
        year, month, day = date.strftime('%Y'), date.strftime('%B'), date.strftime('%d')
        day = day[1] if day[0] == '0' else day
        time.sleep(2)
        driver.execute_script("arguments[0].click();",calendars[i])
        driver.find_element_by_css_selector("button[aria-label = 'Choose month and year'").click()
        driver.find_element_by_css_selector("td[aria-label = '{}']".format(year)).click()
        driver.find_element_by_css_selector("td[aria-label = '{}']".format(month + ' ' + year)).click()
        dt = month + ' ' + day + ',' + ' ' + year
        driver.find_element_by_css_selector("td[aria-label = '{}']".format(dt)).click()


    search = driver.find_element_by_xpath("//*[contains(text(), 'Search')]")
    driver.execute_script("arguments[0].click();", search)
    time.sleep(3)
    
    driver.find_element_by_xpath("//*[contains(text(), 'Download')]").click()
    print('downloading error logs..')
    time.sleep(10)
    downloaded_file_name = dl_path + os.sep + 'Download_CSV.csv'
    
    start_date = start_date.strftime('%d') + start_date.strftime('%b') + start_date.strftime('%y')
    end_date = end_date.strftime('%d') + end_date.strftime('%b') + end_date.strftime('%y')
    new_file_name = dl_path + os.sep + start_date + '_to_' + end_date + ' error logs.csv '
    os.replace(downloaded_file_name,new_file_name)
    return new_file_name