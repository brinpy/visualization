import datetime
from sql_func import create_connection, dbpath
from checker import checkalarm

start = datetime.datetime(2020, 3, 1, 0, 0, 0)
end = datetime.datetime(2020, 3, 28, 22, 59, 59)
checkalarm(bed_str='U' + '580140',fardate=start,closedate=end,connection=create_connection(dbpath),period=1,graph=True, alarm='MF')
