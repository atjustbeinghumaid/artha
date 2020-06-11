import mysql.connector as mysql
import csv
import pandas as pd

def initialize_db():
    db = mysql.connect(
        host = "localhost",
        user = "newuser",
        passwd = "arthadb"
    )
    cursor = db.cursor()
    cursor.execute("SET SQL_MODE='ALLOW_INVALID_DATES'")
    cursor.execute("CREATE DATABASE IF NOT EXISTS artha")
    cursor.execute("USE artha")

    return cursor, db

def commit_error_logs(cursor, db, logfile):
    cursor.execute("CREATE TABLE IF NOT EXISTS error_logs (device_name VARCHAR(255), name VARCHAR(255), inverter_name VARCHAR(255), AlarmID VARCHAR(255), occurrance_time TIMESTAMP, clearance_time TIMESTAMP, message VARCHAR(255), PRIMARY KEY (AlarmID, occurrance_time, clearance_time))")

    query = """INSERT IGNORE into error_logs (device_name, name, inverter_name, AlarmID, occurrance_time, clearance_time, message) VALUES (%s,%s,%s,%s,%s,%s,%s)"""

    with open (logfile, 'r') as f:
        f = f.readlines()[3:]
        reader = csv.reader(f)
        for data in reader:
            cursor.execute(query, data)
        db.commit()

    print("error logs of " + logfile + " committed")

def commit_generation_logs(cursor, db, logfile):

    cursor.execute("""CREATE TABLE IF NOT EXISTS generation_logs (date_recorded DATE, `energy_kWh` DOUBLE(10,2), PRIMARY KEY (date_recorded))""")

    df = pd.read_html(logfile)[0]
    cols = {
        'Category':'date_recorded',
        'Energy Generated in kWh':'energy_kWh'
    }
    df = df.rename(columns = cols)
    # DATE type in mysql uses yyyy-mm-dd format to record dates
    #print(df)
    # df['date_recorded'] = df['date_recorded'].apply(lambda dt: dt.split('/')[2] + '-' + dt.split('/')[1] + '-' + dt.split('/')[0])
    # print(df)
    query = """INSERT IGNORE INTO generation_logs (date_recorded, `energy_kWh`) VALUES (%s, %s)"""
    for _,row in df.iterrows():
        cursor.execute(query, tuple(row))

    db.commit()
    print("energy generation logs of " + logfile + " committed")