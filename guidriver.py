import tkinter as tk
from dbcheck import generateReport
import datetime
from checker import checkalarm
from sql_func import create_connection, truncate, excel_date, convertTime_naive
from supervar import vars
import pathlib
import sys
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
        copylabel.grid(column = 2, row = (1 + thislist.index(i)))
        if thislist.index(i) > 24:
            break

def individual():
    boxinput = lookupbox.get()
    vars.alarm_type = variable.get()
    vars.id = variable2.get()
    checkalarm(bed_str = boxinput, fardate = datetime.datetime.strptime(startentry.get(), '%Y-%m-%d %H:%M:%S'), closedate = datetime.datetime.strptime(endentry.get(), '%Y-%m-%d %H:%M:%S'), connection = connection, period = 1, alarm = vars.alarm_type, graph = True, typeid = vars.id)

def make(howto):
    def _function():
        checkalarm(bed_str=howto[0],fardate=howto[1],closedate=howto[2],connection=howto[3],period=howto[4],graph=howto[5], alarm=howto[6], typeid = howto[7])
    return _function
def genButton(buttontext, bed, commandfunc, buttonrow):
    #print("This shouldn't runs")
    #tk.Button(frame, text = buttontext, command=checkalarm(bed_str=bed,fardate=start,closedate=end,connection=connection,period=1,graph=True, alarm=alarm_type)).pack()
    tk.Button(root, text = buttontext, command=commandfunc, width = 15, anchor = "e", bd = 3, relief ="raised").grid(column = 4, row = buttonrow+1)


root = tk.Tk()
frame = tk.Frame(root)
#frame.pack()
#sdbpath = pathlib.WindowsPath(dbpath)
dbpath = r"C:\Users\brinpy\Documents\sql\alarms.db"
dbpath = r"\\ant\dept-na\FTW1\Support\Facilities\z_Alarms\alarms.db"
print(type(dbpath))
print(dbpath)
connection = create_connection(dbpath)
start = datetime.datetime(2020, 3, 1, 0, 0, 0)
#end = datetime.datetime(2020, 3, 27, 22, 59, 59)


root.iconbitmap('alarm.ico')

root.minsize(width=350, height=200)
version = ('0.1a')
root.title("Alarm Detector - "+ version)
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
startentry.insert(tk.END, str(convertTime_naive(excel_date(datetime.datetime.today()) - 15.0001, 0)))
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