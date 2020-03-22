import sqlite3
import datetime
from sqlite3 import Error
import xlrd
dbpath = r"C:\Users\brinpy\Documents\sql\alarms.db"
def excel_date(date1):
    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")

    except Error as e:
        print(f"The error '{e}' occurred")
    return connection
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        print("With query: " + query)
def convertTime(x, wbOBJ):
    year, month, day, hour, minute, second = xlrd.xldate_as_tuple(x, wbOBJ.datemode)
    return datetime.datetime(year, month, day, hour, minute, second)

def Sort(sub_li): 
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    sub_li.sort(key = lambda x: x[0]) 
    return sub_li 