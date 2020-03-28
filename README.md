# visualization

This program aims to parse data from dematics alarm reported into a sql server, for the ability to preform meaningful trend analysis and gather metrics.


sql_feeder.py parses a .xlx from dematic into the datebase

generatereport() in dbcheck.py currently trends all the data specified to seperate trending data vs converging data and reports the amount of trend, then shows graphs of each bed's performance in descending order

inspect_bed.py allows you to view the data and trend of a single bed
