import os
import datetime
from sql_func import dbpath, create_connection, execute_query, Sort2
from checker import checkalarm

def tryinsert(ls, val, pos):
    if pos is None:
        pos = 0
    if val <= ls[pos]:
        ls.insert(pos, val)
        return ls 
    if val > ls[pos]:
        return tryinsert(ls, val, pos + 1)
    elif val <= ls[pos]:
        ls.insert(pos, val)
        return ls

def generateReport(startd, endd, cxn, period, allowGraph, alarmtype, filterlevel):

    report_table = {}
    report_table_avg = {}
    gettables = "SELECT name FROM sqlite_master where type='table'"
    cur = cxn.cursor()
    cur.execute(gettables)
    table_list = cur.fetchall()
    #print(type(table_list))
    #print(table_list)
    #print(table_list[0][0])
    for tble in table_list:
        #this grabs mf_lat only as checkalarm is only configured to give motor faults
        report_table[tble[0]], report_table_avg[tble[0]] = checkalarm(bed_str=tble[0], fardate=startd, closedate=endd, connection=cxn, period=1,graph=False, alarm = alarmtype)
    lines = []
    #print(report_table)
    for key in report_table:
        if report_table[key] != 0.0 and (report_table_avg[key] > float(filterlevel)):
            lines.append(key + ":  " + str(report_table[key]))

    
    for i in range(len(lines)):
        lines[i] = lines[i].split("  ")
        lines[i][1] = float(lines[i][1])
    sortedList = Sort2(lines)
    #print(sortedList)

    
    
    
    if allowGraph:
        for i in sortedList:
            print(i[0] + "  " + str(i[1]))
        sortedList.reverse()
        for i in sortedList:
            checkalarm(bed_str=i[0].split(":")[0],fardate=startd,closedate=endd,connection=cxn,period=1,graph=True, alarm=alarmtype)
    else:
        sortedList.reverse()
        return sortedList




#start = datetime.datetime(2020, 3, 1, 0, 0, 0)
#end = datetime.datetime(2020, 3, 27, 22, 59, 59)
#cxn = create_connection(dbpath)

#generateReport(start, end, cxn, 1, True)

