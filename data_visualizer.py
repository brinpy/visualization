import matplotlib.pyplot as plt
from sql_func import execute_query, create_connection, convertTime, dbpath, excel_date, Sort, convertTime_naive, months
import os
import datetime
from calendar import monthrange

#records from the DB need to be sorted before they can be used! use sql_func.Sort() !
def visualize(bed_str, fardate, closedate, connection): #dates are passed as datetime datetime objects

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
    area = None
    for row in rows:
        if (row[0] < excel_date(closedate)) and (row[0] > excel_date(fardate)): #date from sql is in range
            time.append(row[0])
            if row[2].split('_').count('MF') > 0: #if motorfault
                mflatch.append(row[0])
            elif row[2].split('_').count('J_LAT') > 0: #if motorfault
                jamlatch.append(row[0])
        area = row[3]
    if actualdays.seconds > 1:
        daysdelta = actualdays.days + 1
    for day in range(daysdelta):
        mflatch_day.append(0)
        jamlatch_day.append(0)
    #print(mflatch_day)
    for day in range(daysdelta):
        for val in mflatch:
            if (convertTime_naive(val, 0) < convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.minute, fardate.second)) + 1 + day, 0)) and (convertTime_naive(val, 0) > convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.minute, fardate.second)) + day, 0)):
               mflatch_day[day] = mflatch_day[day] + 1 
        for val in jamlatch:
            if (convertTime_naive(val, 0) < convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.minute, fardate.second)) + 1 + day, 0)) and (convertTime_naive(val, 0) > convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.minute, fardate.second)) + day, 0)):
               jamlatch_day[day] = jamlatch_day[day] + 1 
    dateay = []
    for day in range(daysdelta):
        dateay.append(convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.minute, fardate.second)) + day + 1, 0))
    
    #print(mflatch_day)


    #plt.style.use('ggplot')
    #fig = plt.figure()
    #ax = fig.plot()
    plt.bar(dateay, mflatch_day)
    plt.plot(dateay, mflatch_day, color = 'red', linewidth = 2)
    dateay_str = []
    #plt.ylim(0,10)
    for i in dateay:
        dateay_str.append(months[i.month] + " " + str(i.day) + ", " + str(i.year))
    if daysdelta > 30:
        for i in range(len(dateay_str)):
            if i%2 > 0:
                dateay_str[i] = ""
            
    plt.xlabel("Occurances")
    plt.ylabel("Day")
    plt.title("Alarm History " + str(daysdelta) + " days, equipment " + str(bed_str) + ", Area: " + area)
    plt.xticks(dateay, dateay_str, rotation = 45)
    #plt.set_xticklabels(dateay_str, rotation = 45)
    #ax.xaxis_date()
    #    print(row)
    #    print(type(row))
    #print(mflatch_day)
    #print(dateay)
    plt.show()


start = datetime.datetime(2020, 3, 1, 0, 0, 0)
end = datetime.datetime(2020, 3, 25, 23, 59, 59)
cxn = create_connection(dbpath)
visualize('U140143', start, end, cxn)

