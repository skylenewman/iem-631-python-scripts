#!/usr/bin/python
import csv
import sys
from datetime import datetime

# 00 - WW.WORK_WORKID AS "A.ID",
# 01 - SW.SUBWORK_SUBWORKID AS "B.ID",
# 02 - SWT.SUBWORKTASK_TASKID AS "C.ID",
# 03 - MT.MAPTASK_MAPID AS "D.ID",
# 04 - MT.MAPTASK_SUBMAPID AS "D.SUB_ID",
# 05 - WM.MAP_MAPID AS "E.ID",
# 06 - SW.SUBWORK_RETURNSUBWORKID AS "B.RETURN_ID",
# 07 - SW.SUBWORK_TITLE AS "B.TITLE",
# 08 - SWT.SUBWORKTASK_TITLE AS "C.TITLE",
# 09 - MT.MAPTASK_TITLE AS "D.TITLE",
# 10 - WM.MAP_TITLE AS "E.TITLE",
# 11 - WW.WORK_STATUS AS "A.STATUS_CD",
# 12 - "A.STATUS",
# 13 - SW.SUBWORK_STATUS AS "B.STATUS_CD",
# 14 - "B.STATUS",
# 15 - SWT.SUBWORKTASK_STATUS AS "C.STATUS_CD",
# 16 - WW.WORK_DATEDUE_MIN AS "A.DATEDUE_MIN",
# 17 - SW.SUBWORK_DATEDUE_MIN AS "B.DATEDUE_MIN",
# 18 - SWT.SUBWORKTASK_DATEDUE_MIN AS "C.DATEDUE_MIN",
# 19 - WW.WORK_DATEDUE_MAX AS "A.DATEDUE_MAX",
# 20 - SW.SUBWORK_DATEDUE_MAX AS "B.DATEDUE_MAX",
# 21 - SWT.SUBWORKTASK_DATEDUE_MAX AS "C.DATEDUE_MAX",
# 22 - WW.WORK_DATEINITIATED AS "A.DATEINITIATED",
# 23 - SW.SUBWORK_DATEINITIATED AS "B.DATEINITIATED",
# 24 - WW.WORK_DATECOMPLETED AS "A.DATECOMPLETED",
# 25 - SW.SUBWORK_DATECOMPLETED AS "B.DATECOMPLETED",
# 26 - SWT.SUBWORKTASK_DATEREADY AS "C.DATEREADY",
# 27 - SWT.SUBWORKTASK_DATEDONE AS "C.DATEDONE",
# 28 - WM.MAP_DUEDURATION AS "E.DUEDURATION",
# 29 - MT.MAPTASK_DUEDURATION AS "D.DUEDURATION",
# 30 - WM.MAP_DUEDATE AS "E.DUEDATE",
# 31 - MT.MAPTASK_DUEDATE AS "D.DUEDATE",
# 32 - WM.MAP_DUETIME AS "E.DUETIME",
# 33 - MT.MAPTASK_DUETIME AS "D.DUETIME",
# 34 - MT.MAPTASK_STARTDATE AS "D.STARTDATE",
# 35 - WW.WORK_OWNERID AS "A.OWNERID",
# 36 - WM.MAP_OWNERID AS "E.OWNERID",
# 37 - MT.MAPTASK_PERFORMERID AS "D.PERFORMERID",
# 38 - WW.WORK_MANAGERID AS "A.MANAGERID",
# 39 - WM.MAP_MANAGERID AS "E.MANAGERID"
#40 "A.DATEDUE_DURATION"
#41 "A.DURATION"
#42 "B.DATEDUE_DURATION"
#43 "B.DURATION"
#44 "C.DATEDUE_DURATION"
#45 "C.DURATION"


datareader = None
workid = 0
workflow_file = None
workflow_writer = None
duedate_list = []
workflow_id_list = []
subworkflow_dictionary = {}
title_list = []
def days_between(d1,d2):
    d1 = datetime.strptime(d1,"%d-%b-%y")
    d2 = datetime.strptime(d2,"%d-%b-%y")
    return abs((d2-d1).days)

def add_to_list(v,l):
    if v not in l:
        l.append(v)
        print v

with open("/Users/kyle/Code/IEM-BIG-DATA/SANITIZED.csv") as infile:
    datareader = csv.reader(infile)
    workid = 0
    count = 0
    for row in datareader:
        # if row[1] not in subworkflow_dictionary:
        #     subworkflow_dictionary[row[1]] = row[0]
        # a_datedue_min = r[18]
        # b_datedue_min = r[19]
        # c_datedue_min = r[20]
        # if a_dd_min is not None and b_dd_min is not None and a_dd_min != '' and b_dd_min != '':
        #     print days_between(a_dd_min,b_dd_min)
        # if a_dd_min is not None and c_dd_min is not None and a_dd_min != '' and c_dd_min != '':
        #     print days_between(a_dd_min,c_dd_min)
        # if c_dd_min is not None and b_dd_min is not None and c_dd_min != '' and b_dd_min != '':
        #     print days_between(c_dd_min,b_dd_min)
        # add_to_list(r[18],duedate_list)
        # add_to_list(r[19],duedate_list)
        # add_to_list(r[20],duedate_list)
        # if r[18] != r[19] or r[19] != r[20]:
        #     print 'INEQUALITY'
        #     print "{} - {} - {}".format(r[18],r[19],r[20])
        if row[7] not in title_list:
            title_list.append(row[7])
            print row[7]
        continue
        if workflow_file is not None:
            if row[0] != workid and workid != 0:
                sys.stdout.write(',')
                workflow_file.close()
                workflow_file = None

        if workflow_file is None:
            if row[0] in subworkflow_dictionary:
                workflow_file = open("/Users/kyle/Code/IEM-BIG-DATA/w/"+subworkflow_dictionary[row[0]]+".csv","a")
            else:
                workflow_file = open("/Users/kyle/Code/IEM-BIG-DATA/w/"+row[0]+".csv","w")
            workflow_writer = csv.writer(workflow_file,delimiter=',')

         # write value
        workid = row[0]
        workflow_writer.writerow(row)
# for s in subworkflow_id_list:
#     if s in workflow_id_list:
#         print "{} in subworkflow_id_list second".format(s)
#     else:
#         print "{} NOT IN subworkflow_id_list".format(s)
# LOOP
# real   	0m31.606s
# user   	0m31.058s
# sys    	0m0.499s

# LOOP AND PRINT
# real   	4m36.964s
# user   	2m56.655s
# sys    	0m22.786s

# INDIVIDUAL FILES
# real   	2m21.056s
# user   	1m18.140s
# sys    	1m2.081s
