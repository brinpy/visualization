from sql_func import execute_query, create_connection, convertTime, excel_date, Sort, convertTime_naive, months
import datetime
import matplotlib.pyplot as plt


def checkalarm(bed_str = '', fardate = '', closedate = '', connection = None, period = 7, alarm = '', graph = True, typeid = ''):
    #print("id = " + typeid)
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
    desc = None
    fault = None
    mfrows = []
    jrows = []
    for row in rows:
        #print("checking rows")
        if (row[0] < excel_date(closedate)) and (row[0] > excel_date(fardate)): #date from sql is in range
            time.append(row[0])
            #print(row)
            if (row[2].split('_').count('MF') > 0) and (alarm == 'MF'): #if motorfault
                #print("appending")
                mflatch.append(row[0])
                mfrows.append(rows.index(row))
                area = row[3]
                desc = row[4]
                fault = row[2]
            elif (row[2].split('_').count('J') > 0) and (alarm == 'J'): #if jam
                jamlatch.append(row[0])
                jrows.append(rows.index(row))
                area = row[3]
                desc = row[4]
                fault = row[2]
    #print("mfs = " + str(len(mflatch)))
    #print("mfrows = " + str(len(mfrows)))
    daysdelta = int(excel_date(closedate) - excel_date(fardate))
    if ((excel_date(closedate) - excel_date(fardate)) % 1) > 0.00000:
        daysdelta = 1 + int(daysdelta)

    for day in range(daysdelta):
        mflatch_day.append(0)
        jamlatch_day.append(0)
    
    #print(mflatch_day)
    for day in range(0, daysdelta, 1):
        #print("thisdate =")
        #print(type(fardate))
        #print(fardate)
        #print(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.hour, fardate.minute, fardate.second))
        #print(convertTime_naive(jamlatch[0], 0))
        #print(convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.minute, fardate.second)), 0))
        #print("now running val in mflatch")
        for val in mflatch:
            
            if (convertTime_naive(val, 0) < convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.hour, fardate.minute, fardate.second)) + 1 + day, 0)) and (convertTime_naive(val, 0) > convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.hour, fardate.minute, fardate.second)) + day, 0)):
                #print("APPENDING VALUE")
                if typeid == 'Duration':
                   mflatch_day[day] += float(rows[mfrows[mflatch.index(val)]][1]) / 1000.0
                elif typeid == 'Frequency':
                    mflatch_day[day] += 1 
        for val in jamlatch:
            if (convertTime_naive(val, 0) < convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.hour, fardate.minute, fardate.second)) + 1 + day, 0)) and (convertTime_naive(val, 0) > convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.hour, fardate.minute, fardate.second)) + day, 0)): 
                if typeid == 'Duration':
                    jamlatch_day[day] += float(rows[jrows[jamlatch.index(val)]][1]) / 1000.0
                elif typeid == 'Frequency':
                    jamlatch_day[day] += 1                    
    dateay = []
    #print("DAYS DELTA = " + str(daysdelta))
    #print(mflatch_day)
    for day in range(daysdelta):
        dateay.append(convertTime_naive(excel_date(datetime.datetime(fardate.year, fardate.month, fardate.day, fardate.hour, fardate.minute, fardate.second)) + day, 0))
    #print(mflatch)
    #print(mflatch_day)
    if alarm == 'MF':
        thisarray = mflatch_day
    elif alarm == 'J':
        thisarray = jamlatch_day
    ####Calculate SMA
    sma = []
    runningTotal = 0
    for day in range(daysdelta):
        
        runningTotal = 0
        if day <= period:
            for i in range(day):
                runningTotal = runningTotal + thisarray[(day - daysdelta) - i]
            if day == 0:
                sma.append(runningTotal)
            else:
                sma.append(runningTotal / (day))
        else:
            for i in range(period):
                runningTotal = runningTotal + thisarray[(day - daysdelta) - i]
            sma.append(runningTotal / (period))

    ####Calculate EMA
    period = 3              #################HMM
    ema = []
    mult = 2/(period + 1)
    for day in range(daysdelta):
        try:
            ema.append(ema[-1] + (mult * (sma[day] - ema[-1])))
        except IndexError:
            ema.append(sma[day])
    ####Calculate Slow EMA
    ema2 = []
    mult = 2/(period*3 + 1)
    for day in range(daysdelta):
        try:
            ema2.append(ema2[-1] + (mult * (sma[day] - ema2[-1])))
        except IndexError:
            ema2.append(sma[day])
    ####calculate histogram
    c = []
    c2 = []
    for i in range(len(ema2)):
        c.append(ema[i] - ema2[i])
        c2.append(ema2[i])
    ###this is to graph
    #print(c)
    if not graph:
        #print("Returned value")
        return c[-1], c2[-1]
    plt.close()
    plt.style.use('dark_background')

    #print(c[-1])
    plt.bar(dateay, thisarray)
    plt.plot(dateay, thisarray, color = 'red', linewidth = 1)
    plt.plot(dateay, sma, color = 'blue', linewidth = 2)
    plt.plot(dateay, ema, color = 'purple', linewidth = 2)
    plt.plot(dateay, ema2, color = 'green', linewidth = 2)
    dateay_str = []
    #plt.ylim(0,10)
    for i in dateay:
        dateay_str.append(months[i.month] + " " + str(i.day) + ", " + str(i.year))
    if daysdelta > 30:
        for i in range(len(dateay_str)):
            if i%2 > 0:
                dateay_str[i] = ""
    j = 0
    #for i in dateay:
    #    print(str(i) + "   " + str(dateay_str[j])) 
    #    j += 1
    plt.xlabel("Date")
    if typeid=='Frequency':
        plt.ylabel("Alarm Occurances")
    elif typeid=='Duration':
        plt.ylabel("Total Alarm Duration (Per Day)")
    if area is None:
        area = "N/A"
    if desc is None:
        desc = "N/A"
    if fault is None:
        fault = "N/A"
    txt = 'BRINPY @ FTW1   BRINPY @ FTW1   BRINPY @ FTW1   BRINPY @ FTW1'

    plt.text(dateay[int(len(dateay) / 2)], int(0.5 * max(thisarray)), txt,
         fontsize=30, color='gray',
         ha='center', va='center', alpha=0.3)
    plt.title("Alarm History " + str(daysdelta) + " days, equipment " + str(bed_str)  + ", Area: " + area + "\n" + fault + ":::" +  desc)
    #print(len(dateay))
    #print(len(mflatch_day))
    #plt.xaxis_date()
    plt.grid(linestyle='-', linewidth='0.5', color='grey')
    plt.xticks(dateay, dateay_str, rotation = 90)
    #plt.set_xticklabels(dateay_str, rotation = 45)
    #ax.xaxis_date()
    #    print(row)
    #    print(type(row))
    plt.subplots_adjust(bottom = .18)
    plt.show()
        
    


#start = datetime.datetime(2020, 3, 1, 0, 0, 0)
#end = datetime.datetime(2020, 3, 25, 22, 59, 59)
#cxn = create_connection(dbpath)
#checkalarm(bed_str='U140143',fardate=start,closedate=end,connection=cxn,period=1,alarm='PID4_MF_LAT')
