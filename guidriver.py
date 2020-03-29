import tkinter as tk
from dbcheck import generateReport
import datetime
from checker import checkalarm
from sql_func import dbpath, create_connection, truncate, excel_date, convertTime_naive
from supervar import vars

choices = ['MF', 'J']
def genReport():
    #get report
    vars.alarm_type = variable.get()
    filterlevel = filterentry.get()
    vars.startDate = datetime.datetime.strptime(startentry.get(), '%Y-%m-%d %H:%M:%S')
    vars.endDate = datetime.datetime.strptime(endentry.get(), '%Y-%m-%d %H:%M:%S')
    print(start)
    print(vars.startDate)
    vars.mainlist = generateReport(vars.startDate, vars.endDate, connection, 1, False, vars.alarm_type, filterlevel)
    thislist = vars.mainlist
    
    

    func_list = []
    for i in vars.mainlist:
        
        inputList = [i[0].split(":")[0], vars.startDate, vars.endDate, connection, 1, True, vars.alarm_type]
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
        if thislist.index(i) > 19:
            break

def individual():
    boxinput = lookupbox.get()
    vars.alarm_type = variable.get()
    checkalarm(bed_str = boxinput, fardate = datetime.datetime.strptime(startentry.get(), '%Y-%m-%d %H:%M:%S'), closedate = datetime.datetime.strptime(endentry.get(), '%Y-%m-%d %H:%M:%S'), connection = connection, period = 1, alarm = vars.alarm_type, graph = True)

def make(howto):
    def _function():
        checkalarm(bed_str=howto[0],fardate=howto[1],closedate=howto[2],connection=howto[3],period=howto[4],graph=howto[5], alarm=howto[6])
    return _function
def genButton(buttontext, bed, commandfunc, buttonrow):
    #print("This shouldn't runs")
    #tk.Button(frame, text = buttontext, command=checkalarm(bed_str=bed,fardate=start,closedate=end,connection=connection,period=1,graph=True, alarm=alarm_type)).pack()
    tk.Button(root, text = buttontext, command=commandfunc, width = 15, anchor = "e", bd = 3, relief ="raised").grid(column = 4, row = buttonrow+1)


root = tk.Tk()
frame = tk.Frame(root)
#frame.pack()
connection = create_connection(dbpath)
start = datetime.datetime(2020, 3, 1, 0, 0, 0)
#end = datetime.datetime(2020, 3, 27, 22, 59, 59)

vars.alarm_type = 'MF'
quitbutton = tk.Button(root, text="QUIT",command=quit, fg='red')

slogan = tk.Button(root,
                   text="Generate Report",
                   command=genReport)
variable = tk.StringVar(root)
variable.set(choices[0])
w = tk.OptionMenu(root, variable, "MF", "J")
w.grid(column=1,row=6)

startlabel = tk.Label(root, text = "Start Date (Y-M-D)= ", anchor = 'w')
endlabel = tk.Label(root, text = "End Date (Y-M-D)= ", anchor = 'w')
specific = tk.Button(root, text = "Bed lookup ->", relief ="raised", command=individual)
filterlabel = tk.Label(root, text = "Filter AVG > ")
filterentry = tk.Entry(root)
filterentry.insert(tk.END, "1")

startentry = tk.Entry(root)
startentry.insert(tk.END, str(convertTime_naive(excel_date(datetime.datetime.today()) - 15, 0)))
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

root.mainloop()