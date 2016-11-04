#!/usr/bin/python
import csv
import re
from datetime import datetime
import os

datareader = None
workid = 0

def add_to_list(v,l):
    if v not in l:
        l.append(v)
        print v

def add_to_dict_list(my_list,key,val):
    if key is not None and key != '' and val is not None and val != '':
        if key in my_list:
            tmp = my_list[key]
            if val is not None and val not in tmp:
                tmp.append(val)
                my_list[key] = tmp
            else:
                pass
        else:
            my_list[key] = [val]

def write_dictionary(my_dict,subdir=''):
    for k in my_dict:
        filename = k
        filename = filename.replace(" ","")
        directory = "/Users/kyle/Code/IEM-BIG-DATA/i/" + subdir + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        index_file = open(directory + filename+".csv","w")
        for wf_id in my_dict[k]:
            index_file.write(wf_id)
            index_file.write('\n')
        index_file.close()


def get_month_as_decimal(d):
    if d is not None and d != '':
        try:
            d = datetime.strptime(d,"%d-%b-%y")
            return d.strftime("%m")
        except ValueError:
            return ''
    else:
        return ''

def get_year_with_century(d):
    if d is not None and d != '':
        try:
            d = datetime.strptime(d,"%d-%b-%y")
            return d.strftime("%Y")
        except ValueError:
            return ''
    else:
        return ''

def days_between(d1,d2):
    if d1 is not None and d1 != '':
        try:
            d1 = datetime.strptime(d1,"%d-%b-%y")
            if d2 is None or d2 == '':
                d2 = now
            else:
                d2 = datetime.strptime(d2,"%d-%b-%y")
            return abs((d2-d1).days)
        except ValueError:
            return ''

def get_day_of_year(d):
    if d is not None and d != '':
        try:
            d = datetime.strptime(d,"%d-%b-%y")
            return d.strftime("%j")
        except ValueError:
            return ''
    else:
        return ''


# INDEX DICTIONARIES
workflowtype___workflows_dictionary = {}
workflowtype_workflowstatus___workflows_dictionary = {}
workflowstatus___workflows_dictionary = {}
workflowstatus_incomplete___workflows_dictionary = {}
workflowstatus_complete___workflows_dictionary = {}
a_ownerid___workflows_dictionary = {}
e_ownerid___workflows_dictionary = {}
monthinitiated___workflows_dictionary = {}
yearinitiated___workflows_dictionary = {}
yearinitiated_monthinitated__workflows_dictionary = {}
dayofyearinitiated___workflows_dictionary = {}
monthcompleted___workflows_dictionary = {}
yearcompleted___workflows_dictionary = {}
yearcompleted_monthcompleted___workflows_dictionary = {}
yearinitiated_workflowtype___workflows_dictionary = {}
monthinitiated_workflowtype___workflows_dictionary = {}
yearinitiated_monthinitiated_workflowtype___workflows_dictionary = {}
dayofyearinitiated_workflowtype___workflows_dictionary = {}
yearcompleted_workflowtype___workflows_dictionary = {}
monthcompleted_workflowtype___workflows_dictionary = {}
yearcompleted_monthcompleted_workflowtype___workflows_dictionary = {}
duration___workflows_dictionary = {}
duration_workflowtype___workflows_dictionary = {}

with open("/Users/kyle/Code/IEM-BIG-DATA/DIFFS.csv") as infile:
    now = datetime.now()
    datareader = csv.reader(infile)
    workid = 0
    print 'FILE OPEN; LOOPING OVER ROWS'
    for row in datareader:
        if workid != row[0]:
            # WORKFLOW TYPE AND STATUS
            add_to_dict_list(workflowtype___workflows_dictionary,row[7],row[0])
            add_to_dict_list(workflowstatus___workflows_dictionary,row[12],row[0])
            add_to_dict_list(workflowtype_workflowstatus___workflows_dictionary,"{}:{}".format(row[7],row[12]),row[0])
            if row[11] != '-1' and row[11] != '-2' and row[11] != '-3':
                add_to_dict_list(workflowstatus_incomplete___workflows_dictionary,'incomplete-workflows',row[0])
            if row[11] == '-1' or row[11] == '-2' or row[11] == '-3':
                add_to_dict_list(workflowstatus_complete___workflows_dictionary,'complete-workflows',row[0])

            # WORKFLOW USERS
            add_to_dict_list(a_ownerid___workflows_dictionary,row[35],row[0])
            add_to_dict_list(e_ownerid___workflows_dictionary,row[36],row[0])

            # INITIATED DATE TO INDIVIDUAL WORKFLOWS
            add_to_dict_list(monthinitiated___workflows_dictionary,"i::::{}:".format(get_month_as_decimal(row[22])),row[0])
            add_to_dict_list(yearinitiated___workflows_dictionary,"i{}:::".format(get_year_with_century(row[22])),row[0])
            add_to_dict_list(yearinitiated_monthinitated__workflows_dictionary,"i{}:{}:".format(get_year_with_century(row[22]),get_month_as_decimal(row[22])),row[0])
            add_to_dict_list(dayofyearinitiated___workflows_dictionary,"j{}".format(get_day_of_year(row[22])),row[0])

            # COMPLETED DATE TO INDIVIDUAL WORKFLOWS
            add_to_dict_list(monthcompleted___workflows_dictionary,"c::::{}:".format(get_month_as_decimal(row[24])),row[0])
            add_to_dict_list(yearcompleted___workflows_dictionary,"c{}:::".format(get_year_with_century(row[24])),row[0])
            add_to_dict_list(yearcompleted_monthcompleted___workflows_dictionary,"c{}:{}:".format(get_year_with_century(row[24]),get_month_as_decimal(row[24])),row[0])

            # INITIATED DATE AND WORKFLOWTYPE TO WORKFLOWS
            add_to_dict_list(yearinitiated_workflowtype___workflows_dictionary,"i{}::::{}".format(get_year_with_century(row[22]),row[7]),row[0])
            add_to_dict_list(monthinitiated_workflowtype___workflows_dictionary,"i:::::{}:{}".format(get_month_as_decimal(row[22]),row[7]),row[0])
            add_to_dict_list(yearinitiated_monthinitiated_workflowtype___workflows_dictionary,"i{}:{}:{}".format(get_year_with_century(row[22]),get_month_as_decimal(row[22]),row[7]),row[0])
            add_to_dict_list(dayofyearinitiated_workflowtype___workflows_dictionary,"j{}:{}".format(get_day_of_year(row[22]),row[7]),row[0])

            # COMPLETED DATE AND WORKFLOWTYPE TO WORKFLOWS
            add_to_dict_list(yearcompleted_workflowtype___workflows_dictionary,"c{}::::{}".format(get_year_with_century(row[25]),row[7]),row[0])
            add_to_dict_list(monthcompleted_workflowtype___workflows_dictionary,"c:::::{}:{}".format(get_month_as_decimal(row[25]),row[7]),row[0])
            add_to_dict_list(yearcompleted_monthcompleted_workflowtype___workflows_dictionary,"c{}:{}:{}".format(get_year_with_century(row[25]),get_month_as_decimal(row[25]),row[7]),row[0])

            # DURATION
            add_to_dict_list(duration___workflows_dictionary,"d{}".format(days_between(row[22],row[25])),row[0])
            add_to_dict_list(duration_workflowtype___workflows_dictionary,"d{}:{}".format(days_between(row[25],row[25]),row[7]),row[0])


            workid = row[0]
infile.close()

write_dictionary(workflowtype___workflows_dictionary,'a.type')
write_dictionary(workflowstatus___workflows_dictionary,'a.status')
write_dictionary(workflowtype_workflowstatus___workflows_dictionary,'a.status_type')
write_dictionary(workflowstatus_incomplete___workflows_dictionary)
write_dictionary(workflowstatus_complete___workflows_dictionary)
write_dictionary(a_ownerid___workflows_dictionary,'a.owner_id')
write_dictionary(e_ownerid___workflows_dictionary,'e.owner_id')
write_dictionary(monthinitiated___workflows_dictionary,'m.init')
write_dictionary(yearinitiated___workflows_dictionary,'y.init')
write_dictionary(yearinitiated_monthinitated__workflows_dictionary,'y_m.init')
write_dictionary(dayofyearinitiated___workflows_dictionary,'j.init')
write_dictionary(monthcompleted___workflows_dictionary,'m.comp')
write_dictionary(yearcompleted___workflows_dictionary,'y.comp')
write_dictionary(yearcompleted_monthcompleted___workflows_dictionary,'y_m.comp')
write_dictionary(yearinitiated_workflowtype___workflows_dictionary,'y.init.type')
write_dictionary(monthinitiated_workflowtype___workflows_dictionary,'m.init.type')
write_dictionary(yearinitiated_monthinitiated_workflowtype___workflows_dictionary,'y_m.init.type')
write_dictionary(dayofyearinitiated_workflowtype___workflows_dictionary,'j.init')
write_dictionary(yearcompleted_workflowtype___workflows_dictionary,'y.comp.type')
write_dictionary(monthcompleted_workflowtype___workflows_dictionary,'m.comp.type')
write_dictionary(yearcompleted_monthcompleted_workflowtype___workflows_dictionary,'y_m.comp.type')
write_dictionary(duration___workflows_dictionary,'duration')
write_dictionary(duration_workflowtype___workflows_dictionary,'duration.type')
