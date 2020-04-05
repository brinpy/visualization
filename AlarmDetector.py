import tkinter as tk
from dbcheck import generateReport
import datetime
from checker import checkalarm
from sql_func import create_connection, truncate, excel_date, convertTime_naive
from supervar import vars
import pathlib
import sys

version = ('0.3a')
rowsLimit = 24
a = '''
dbpath = ''
def createfilefunc():
    f = open("dbpath.txt", 'x')
    f.write(pathentry.get())
    dbpath = pathentry.get()
    f.close()
    quit

try:
    fileo = open("dbpath.txt", 'r')
    dbpath = fileo.read()
    print(dbpath)
    fileo.close()
except FileNotFoundError:
    root0 = tk.Tk()
    pathlabel = tk.Label(root0, text = 'Enter database path below')
    pathentry = tk.Entry(root0)
    pathcontinue = tk.Button(root0, text = "Continue", command=createfilefunc)
    pathlabel.grid(column=1, row=1)
    pathentry.grid(column=1, row=2)
    pathcontinue.grid(column=1,row=3)
    root0.mainloop()
   '''

    

#dbpath = r"C:\Users\brinpy\Documents\sql\alarms.db"

choices = ['MF', 'J']
choices2 = ["Frequency", "Duration"]

#welcome to global variables, RIP
spacelist = []
def genReport():
    #get report
    vars.alarm_type = variable.get()
    vars.id = variable2.get()
    filterlevel = filterentry.get()
    vars.startDate = datetime.datetime.strptime(startentry.get(), '%Y-%m-%d %H:%M:%S')
    vars.endDate = datetime.datetime.strptime(endentry.get(), '%Y-%m-%d %H:%M:%S')

    vars.mainlist = generateReport(vars.startDate, vars.endDate, connection, 1, False, vars.alarm_type, filterlevel, vars.id)
    thislist = vars.mainlist
    
    

    func_list = []
    for i in vars.mainlist:
        
        inputList = [i[0].split(":")[0], vars.startDate, vars.endDate, connection, 1, True, vars.alarm_type, vars.id]
        func_obj = make(inputList)
        #print("obj added")
        #print(type(func_obj))
        #print(func_obj)
        func_list.append(func_obj)

    #gen_functions(thislist)
    #print(func_list)
    for i in thislist:
        t = i[0] + "  " + str(truncate(i[1], 3))
        genButton(t, i[0].split(":")[0], func_list[thislist.index(i)], thislist.index(i))
        if (1+ thislist.index(i)) > 6:
            copylabel.grid(column = 2, row = (2 + thislist.index(i)))
        else:
            copylabel.grid(column = 2, row = 7)
        if thislist.index(i) > rowsLimit:
            break
mylabels = [[],[],[],[],[]]
def individual():
    global spacelist #uh oh
    boxinput = lookupbox.get()
    vars.alarm_type = variable.get()
    vars.id = variable2.get()
    pltobj, rows = checkalarm(bed_str = boxinput, fardate = datetime.datetime.strptime(startentry.get(), '%Y-%m-%d %H:%M:%S'), closedate = datetime.datetime.strptime(endentry.get(), '%Y-%m-%d %H:%M:%S'), connection = connection, period = 1, alarm = vars.alarm_type, graph = True, typeid = vars.id)
    rows.reverse()
    timeW = 0
    descW = 0
    durW = 0
    areaW = 0
    typeW = 0
    mylabels = [[],[],[],[],[]]
    listslaves = tablelistFrame.grid_slaves()
    for l in listslaves:
        l.destroy()
    tk.Label(tablelistFrame, anchor = "center", text = "Time").grid(column = 4, row = 1)
    tk.Label(tablelistFrame, anchor = "center", text = "\u0394T").grid(column = 5, row = 1)
    tk.Label(tablelistFrame, anchor = "center", text = "Description").grid(column = 6, row = 1)
    tk.Label(tablelistFrame, anchor = "center", text = "Alarm Type").grid(column = 7, row = 1)
    tk.Label(tablelistFrame, anchor = "center", text = "Area").grid(column = 8, row = 1)
    for i in rows:
        timeW = len(str(convertTime_naive(i[0], 0))) if timeW < len(str(convertTime_naive(i[0], 0))) else timeW
        descW = len(i[4]) if descW < len(i[4]) else descW
        durW = len(str(i[1] / 1000)) if durW < len(str(i[1] / 1000)) else durW
        areaW = len(i[3]) if areaW < len(i[3]) else areaW
        typeW = len(i[2]) if typeW < len(i[2]) else typeW
        if rows.index(i) > rowsLimit:
            break
    for i in rows:
        mylabels[0].append(tk.Label(tablelistFrame,relief = "ridge", text = str(convertTime_naive(i[0], 0)), width = timeW + 1))
        mylabels[1].append(tk.Label(tablelistFrame,relief = "ridge", text = str(i[1]/1000) + 's', width = durW + 1))
        mylabels[2].append(tk.Label(tablelistFrame,relief = "ridge", text = i[4], width = descW + 1))
        mylabels[3].append(tk.Label(tablelistFrame,relief = "ridge", text = i[2], width = typeW + 1))
        mylabels[4].append(tk.Label(tablelistFrame,relief = "ridge", text = i[3], width = areaW + 1))
        if rows.index(i) > rowsLimit:
            break
    for i in range(len(mylabels)):
        for j in range(len(mylabels[0])):
            mylabels[i][j].grid(column = i + 4, row = j + 2)
    for widget in spacelist:
        widget.destroy()
    spacelist = []
    if len(rows) > 7:
        for i in range(6, len(rows) - 3): ###make sure to copy this to the make function
            spacelist.append(tk.Label(root, text = ''))
            spacelist[-1].grid(column = 2, row = i)
            if i > rowsLimit:
                break
        copylabel.grid(column = 2, row = len(rows))
    pltobj.show()
def make(howto):
    def _function():
        pltobj, rows = checkalarm(bed_str=howto[0],fardate=howto[1],closedate=howto[2],connection=howto[3],period=howto[4],graph=howto[5], alarm=howto[6], typeid = howto[7])
        rows.reverse()
        global spacelist
        timeW = 0
        descW = 0
        durW = 0
        areaW = 0
        typeW = 0
        mylabels = [[],[],[],[],[]]
        listslaves = tablelistFrame.grid_slaves()
        for l in listslaves:
            l.destroy()
        tk.Label(tablelistFrame, anchor = "center", text = "Time").grid(column = 4, row = 1)
        tk.Label(tablelistFrame, anchor = "center", text = "\u0394T").grid(column = 5, row = 1)
        tk.Label(tablelistFrame, anchor = "center", text = "Description").grid(column = 6, row = 1)
        tk.Label(tablelistFrame, anchor = "center", text = "Alarm Type").grid(column = 7, row = 1)
        tk.Label(tablelistFrame, anchor = "center", text = "Area").grid(column = 8, row = 1)
        for i in rows:
            timeW = len(str(convertTime_naive(i[0], 0))) if timeW < len(str(convertTime_naive(i[0], 0))) else timeW
            descW = len(i[4]) if descW < len(i[4]) else descW
            durW = len(str(i[1] / 1000)) if durW < len(str(i[1] / 1000)) else durW
            areaW = len(i[3]) if areaW < len(i[3]) else areaW
            typeW = len(i[2]) if typeW < len(i[2]) else typeW
            if rows.index(i) > rowsLimit:
                break
        for i in rows:
            mylabels[0].append(tk.Label(tablelistFrame,relief = "ridge", text = str(convertTime_naive(i[0], 0)), width = timeW + 1))
            mylabels[1].append(tk.Label(tablelistFrame,relief = "ridge", text = str(i[1]/1000) + 's', width = durW + 1))
            mylabels[2].append(tk.Label(tablelistFrame,relief = "ridge", text = i[4], width = descW + 1))
            mylabels[3].append(tk.Label(tablelistFrame,relief = "ridge", text = i[2], width = typeW + 1))
            mylabels[4].append(tk.Label(tablelistFrame,relief = "ridge", text = i[3], width = areaW + 1))
            if rows.index(i) > rowsLimit:
                break
        for i in range(len(mylabels)):
            for j in range(len(mylabels[0])):
                mylabels[i][j].grid(column = i + 4, row = j + 2)
        for widget in spacelist:
            widget.destroy()
        spacelist = []
        if len(rows) > 7:
            for i in range(6, len(rows) - 3): ###make sure to copy this to the make function
                spacelist.append(tk.Label(root, text = ''))
                spacelist[-1].grid(column = 2, row = i)
                if i > rowsLimit:
                    break
        if len(rows) > 7:
            copylabel.grid(column = 2, row = len(rows))
        else:
            copylabel.grid(column = 2, row = 7)
        pltobj.show()
    return _function
def genButton(buttontext, bed, commandfunc, buttonrow):
    #print("This shouldn't runs")
    #tk.Button(frame, text = buttontext, command=checkalarm(bed_str=bed,fardate=start,closedate=end,connection=connection,period=1,graph=True, alarm=alarm_type)).pack()
    tk.Button(root, text = buttontext, command=commandfunc, width = 15, anchor = "e", bd = 3, relief ="raised").grid(column = 3, row = buttonrow+1)


rootA = tk.Tk()
root = tk.Frame(rootA)
root.pack(side = "left")
tablelistFrame = tk.Frame(rootA)
tablelistFrame.pack(side = "right")
#emptyframe = tk.Frame(rootA)
#emptyframe.pack(side = "bottom")
#tk.Label(emptyframe, text = "").grid(column = 1, row = 1)
#frame.pack()
#sdbpath = pathlib.WindowsPath(dbpath)
dbpath = r"C:\Users\brinpy\Documents\sql\alarms.db"
dbpath = r"\\ant\dept-na\FTW1\Support\Facilities\z_Alarms\alarms.db"
#print(type(dbpath))
print(dbpath)
connection = create_connection(dbpath)
start = datetime.datetime(2020, 3, 1, 0, 0, 0)
#end = datetime.datetime(2020, 3, 27, 22, 59, 59)


rootA.iconbitmap('alarm.ico')

rootA.minsize(width=350, height=200)

rootA.title("Alarm Detector - " + version)
mytxt = "Made by BRINPY @ FTW1"
copylabel = tk.Label(root, text = mytxt)

vars.alarm_type = 'MF'
quitbutton = tk.Button(root, text="QUIT",command=sys.exit, fg='red')

slogan = tk.Button(root,
                   text="Generate Report",
                   command=genReport)
variable = tk.StringVar(root)
variable2 = tk.StringVar(root)
variable.set(choices[0])
variable2.set(choices2[0])
w = tk.OptionMenu(root, variable, "MF", "J")
w2 = tk.OptionMenu(root, variable2, "Frequency", "Duration")
w.grid(column=1,row=6)
w2.grid(column = 1, row = 7)
startlabel = tk.Label(root, text = "Start Date (Y-M-D)= ", anchor = 'w')
endlabel = tk.Label(root, text = "End Date (Y-M-D)= ", anchor = 'w')
specific = tk.Button(root, text = "Bed lookup ->", relief ="raised", command=individual)
filterlabel = tk.Label(root, text = "Filter AVG > ")
filterentry = tk.Entry(root)
filterentry.insert(tk.END, "1")

startentry = tk.Entry(root)
startentry.insert(tk.END, str(convertTime_naive(int(excel_date(datetime.datetime.today()) - 15), 0)))
endentry = tk.Entry(root)
endentry.insert(tk.END, str(convertTime_naive(excel_date(datetime.datetime.today()), 0)))
lookupbox = tk.Entry(root)
slogan.grid(row=1, column=2)

quitbutton.grid(row=1, column=1)
#tk.Button(root, text = "test", command=quit).grid(row=1,column=1)
startlabel.grid(column = 1, row = 2)
startentry.grid(column = 2, row = 2)
endlabel.grid(column = 1, row = 3)
endentry.grid(column = 2, row = 3)
specific.grid(column = 1, row = 5)
lookupbox.grid(column = 2, row = 5)
filterentry.grid(column = 2, row = 4)
filterlabel.grid(column = 1, row = 4)
copylabel.grid(column = 2, row = 100)
root.mainloop()