#!/usr/bin/python
import csv
import json
import re
from datetime import datetime

datareader = None
workid = 0
workflow_file = None
workflow_writer = None
duedate_list = []
workflow_id_list = []

with open("/Users/kyle/Code/IEM-BIG-DATA/DIFFS.csv") as infile:
    datareader = csv.reader(infile)
    workid = 0
    count = 0
    print 'FILE OPEN; LOOPING OVER ROWS'
    for row in datareader:
        if workflow_file is not None:
            if row[0] != workid and workid != 0:
                workflow_file.close()
                workflow_file = None

        if workflow_file is None:
            workflow_file = open("/Users/kyle/Code/IEM-BIG-DATA/w/"+row[0]+".csv","w")
            workflow_writer = csv.writer(workflow_file,delimiter=',')

         # write value
        workflow_writer.writerow(row)
        workid = row[0]
