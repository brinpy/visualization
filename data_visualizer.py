import matplotlib
from sql_func import execute_query, create_connection, convertTime, dbpath, excel_date, Sort
import os
import datetime
from calendar import monthrange

#records from the DB need to be sorted before they can be used! use sql_func.Sort() !
def visualize(bed_str, fardate, closedate, connection, scale_days = 1): #dates are passed as datetime datetime objects

    selectable = "SELECT * FROM " + bed_str + " WHERE time >= " + str(excel_date(fardate)) + " AND time <= " + str(excel_date(closedate)) + ";" 

    cur = connection.cursor()
    #print(type(selectable))
    #print(type(connection))
    cur.execute(selectable)
    rows = cur.fetchall()
    rows = Sort(rows)
    #rows.reverse()

    #generate plot data
    time = []
    jamlatch = []
    jamlatch_day = []
    mflatch = []
    mflatch_day = []
    actualdays = closedate - fardate
    for row in rows:
        if (row[0] < excel_date(closedate)) and (row[0] > excel_date(fardate)): #date from sql is in range
            time.append(row[0])
            if row[2].split('_').count('MF') > 0: #if motorfault
                mflatch.append(row[0])
            elif row[2].split('_').count('J_LAT') > 0: #if motorfault
                jamlatch.append(row[0])
    if actualdays.seconds > 1:
        daysdelta = actualdays.days + 1
    for day in range(daysdelta):
        mflatch_day.append(0)
        jamlatch_day.append(0)
    for day in range(daysdelta):
        for val in mflatch_day:
            d___, d_ = monthrange(fardate.year, fardate.month)

            if fardate.month
            if (val < excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day + day + 1, fardate.minute, fardate.second))) and (val > excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day + day, fardate.minute, fardate.second))):
               mflatch_day[day] = mflatch_day[day] + 1 
        for val in jamlatch_day:
            if (val < excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day + day + 1, fardate.minute, fardate.second))) and (val > excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day + day, fardate.minute, fardate.second))):
               jamlatch_day[day] = jamlatch_day[day] + 1 
    #    print(row)
    #    print(type(row))
    print(mflatch_day)



start = datetime.datetime(2020, 2, 1, 0, 0, 0)
end = datetime.datetime(2020, 3, 18, 23, 59, 59)
cxn = create_connection(dbpath)
visualize('U140143', start, end, cxn)
