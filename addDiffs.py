#!/usr/bin/python
import csv
from datetime import datetime

datareader = None
now = datetime.now()
def days_between(d1,d2):
    try:
        d1 = datetime.strptime(d1,"%d-%b-%y")
        if d2 is None or d2 == '':
            d2 = now
        else:
            d2 = datetime.strptime(d2,"%d-%b-%y")
        return abs((d2-d1).days)
    except ValueError:
        return ''
def f(x):
    returnValue = ''
    if x == '1': returnValue = 'WAITING'
    elif x == '2': returnValue = 'READY'
    elif x == '3': returnValue = 'STARTED'
    elif x == '4': returnValue = 'SUSPENDED'
    elif x == '5': returnValue = 'EXECUTING'
    elif x == '-1': returnValue = 'DONE'
    elif x == '-2': returnValue = 'KILLED'
    elif x == '-3': returnValue = 'FINISHED'
    elif x == '-4': returnValue = 'DELETED'
    return returnValue


with open("/Users/kyle/Code/IEM-BIG-DATA/SANITIZED.csv") as infile:
    datareader = csv.reader(infile)

    diff_file = open("/Users/kyle/Code/IEM-BIG-DATA/DIFFSsdfghjk.csv","w")
    diff_writer = csv.writer(diff_file,delimiter=',')


    for row in datareader:
        new_rows = []

        # 16 - "A.DATEDUE_MIN",
        # 19 - "A.DATEDUE_MAX",
        new_rows.append(days_between(row[16],row[19])) #40

        # 22 - "A.DATEINITIATED",
        # 24 - "A.DATECOMPLETED",
        new_rows.append(days_between(row[22],row[24])) #41

        # 17 - "B.DATEDUE_MIN",
        # 20 - "B.DATEDUE_MAX",
        new_rows.append(days_between(row[17],row[20])) #42

        # 23 - "B.DATEINITIATED",
        # 25 - "B.DATECOMPLETED",
        new_rows.append(days_between(row[23],row[25])) #43

        # 18 - "C.DATEDUE_MIN",
        # 21 - "C.DATEDUE_MAX",
        new_rows.append(days_between(row[18],row[21])) #44

        # 26 - "C.DATEREADY",
        # 27 - "C.DATEDONE",
        new_rows.append(days_between(row[26],row[27])) #45

        # C.STATUS
        new_rows.append(f(row[15])) #46

         # write value
        diff_writer.writerow(row+new_rows)

    diff_file.close()
