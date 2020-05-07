from sqlite3 import Error
import os
import xlrd
from sql_func import execute_query, create_connection, convertTime
import time
file = r'C:\Users\brinpy\Downloads\AlarmsHistory.xls'
wb = xlrd.open_workbook(file) 
sheet = wb.sheet_by_index(0) 

dbpath = r"C:\Users\brinpy\Documents\sql\alarms.db"
dbpath = r"\\ant\dept-na\FTW1\Support\Facilities\z_Alarms\alarms.db"
connection = create_connection(dbpath)
row = 9
cur = connection.cursor()
countme = 0
runagain = True
lasttime = int(time.time() * 1000)
while runagain:
    if countme % 100 == 0:
        countme += 1
        print("Processed " + str(countme) + " records in " + str((time.time()*1000) - lasttime) + " ms")
        lasttime = int(time.time() * 1000)

    else:
        countme += 1
    if sheet.cell_value(row, 0) == sheet.cell_value(-1, 0):
        runagain = False
        print("END OF FILE")
    tag = sheet.cell_value(row, 10)
    tag = tag.split('_')
    tagcompare = list(tag[0])[0]
    if (tagcompare == 'U') or (list(tag[0])[0]) == 'C' or (list(tag[0])[0] == 'R'):
        #print("Allowable tag")
        tblename = tag[0]
        tag.pop(0)
        alarm_type_str = '_'
        alarm_type_str = alarm_type_str.join(tag)
        #print(tag)
        time_val = sheet.cell_value(row, 0)
        duration_ms = int(sheet.cell_value(row, 1) * 1000)
        area_str = sheet.cell_value(row, 7)
        description_str = sheet.cell_value(row, 3)
        #print(list(alarm_type_str))
        #if row > 10:
        create_alarm_table = "CREATE TABLE IF NOT EXISTS " + tblename + " (time FLOAT(23), duration_ms INTEGER, alarm_type varchar(50), area varchar(50), description varchar(255));"
        
        lis = list(description_str.split("'"))
        
        description_str2 = ''.join(lis)
        create_alarm = "INSERT INTO " + tblename + " (time, duration_ms, alarm_type, area, description) VALUES ('" + str(time_val) + "', " + str(duration_ms) + ", '" + alarm_type_str + "', '" + area_str + "', '" + description_str2 + "');"
        if row < 0:
            print(create_alarm_table)
            print(create_alarm)
            print(row)
        execute_query(connection, create_alarm_table)

        selectable = "SELECT * FROM " + tblename + " WHERE time = " + str(time_val) + ";"
        cur.execute(selectable)
        possibleduplicate = cur.fetchall()
        runquery = True
        for i in possibleduplicate:
            if (int(i[1]) == duration_ms) and (i[4] == description_str):
                runquery = False
                break

        
        if runquery: 
            execute_query(connection, create_alarm)
        #print("completed query")
    row += 1
    
        




 
#execute_query(connection, create_alarm_table)
#execute_query(connection, create_alarm)
os.remove(file)