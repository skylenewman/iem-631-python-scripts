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
    if d1 is not None and d2 is not None and d1 != '' and d2 != '':
        try:
            d1 = datetime.strptime(d1,"%d-%b-%y")
            d2 = datetime.strptime(d2,"%d-%b-%y")
            return abs((d2-d1).days)
        except ValueError:
    return ''


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
        # print my_list

def fd(s):
    if s is not None and s != '':
        return s
    else:
        return '         '

def write_index(webster,file_name):
    for k in webster:
        key = re.sub('[^0-9a-zA-Z]+', '', k)
        with open('/Users/kyle/Code/IEM-BIG-DATA/'+file_name+'-'+key+'.json', 'w') as fp:
            json.dump(webster[k], fp)


# INDEX DICTIONARIES
workflowtype___workflows_dictionary = {}
workflowstatus___workflows_dictionary = {}
workfowstatus_workflowtype___workflows_dictionary = {}
a_ownerid___workflows_dictionary = {}
e_ownerid___workflows_dictionary = {}

monthinitiated___workflows_dictionary = {}
yearinitiated___workflows_dictionary = {}
yearinitiated_monthinitated__workflows_dictionary = {}

monthcompleted___workflows_dictionary = {}
yearcompleted___workflows_dictionary = {}
yearcompleted_monthcompleted___workflows_dictionary = {}

yearinitiated_workflowtype___workflows_dictionary = {}
monthinitiated_workflowtype___workflows_dictionary = {}
yearinitiated_monthinitiated_workflowtype___workflows_dictionary = {}

yearcompleted_workflowtype___workflows_dictionary = {}
monthcompleted_workflowtype___workflows_dictionary = {}
yearcompleted_monthcompleted_workflowtype___workflows_dictionary = {}

directory = '/Users/kyle/Code/IEM-BIG-DATA/'
if not os.path.exists(directory):
    os.makedirs(directory)

with open("/Users/kyle/Code/IEM-BIG-DATA/DIFFS.csv") as infile:
    datareader = csv.reader(infile)
    workid = 0
    count = 0
    print 'FILE OPEN; LOOPING OVER ROWS'
    for row in datareader:
        if workid != row[0]:

            add_to_dict_list(workflowtype___workflows_dictionary,row[7],row[0])
            # add_to_dict_list(workflowstatus___workflows_dictionary,row[12],row[0])
            # add_to_dict_list(workfowstatus_workflowtype___workflows_dictionary,"{}:{}".format(row[12],row[7]),row[0])
            # add_to_dict_list(a_ownerid___workflows_dictionary,row[37],row[0])
            # add_to_dict_list(e_ownerid___workflows_dictionary,row[38],row[0])
            # # INITIATED DATE TO INDIVIDUAL WORKFLOWS
            # add_to_dict_list(monthinitiated___workflows_dictionary,"::::{}:".format(get_month_as_decimal(row[23])),row[0])
            # add_to_dict_list(yearinitiated___workflows_dictionary,"{}:::".format(get_year_with_century(row[23])),row[0])
            # add_to_dict_list(yearinitiated_monthinitated__workflows_dictionary,"{}:{}:".format(get_year_with_century(row[23]),get_month_as_decimal(row[23])),row[0])
            # # COMPLETED DATE TO INDIVIDUAL WORKFLOWS
            # add_to_dict_list(monthcompleted___workflows_dictionary,"::::{}:".format(get_month_as_decimal(row[25])),row[0])
            # add_to_dict_list(yearcompleted___workflows_dictionary,"{}:::".format(get_year_with_century(row[25])),row[0])
            # add_to_dict_list(yearcompleted_monthcompleted___workflows_dictionary,"{}:{}:".format(get_year_with_century(row[25]),get_month_as_decimal(row[25])),row[0])
            # # INITIATED DATE AND WORKFLOWTYPE TO WORKFLOWS
            # add_to_dict_list(yearinitiated_workflowtype___workflows_dictionary,"{}::::{}".format(get_year_with_century(row[23]),row[7]),row[0])
            # add_to_dict_list(monthinitiated_workflowtype___workflows_dictionary,":::::{}:{}".format(get_month_as_decimal(row[23]),row[7]),row[0])
            # add_to_dict_list(yearinitiated_monthinitiated_workflowtype___workflows_dictionary,"{}:{}:{}".format(get_year_with_century(row[23]),get_month_as_decimal(row[23]),row[7]),row[0])
            # # COMPLETED DATE AND WORKFLOWTYPE TO WORKFLOWS
            # add_to_dict_list(yearcompleted_workflowtype___workflows_dictionary,"{}::::{}".format(get_year_with_century(row[25]),row[7]),row[0])
            # add_to_dict_list(monthcompleted_workflowtype___workflows_dictionary,":::::{}:{}".format(get_month_as_decimal(row[25]),row[7]),row[0])
            # add_to_dict_list(yearcompleted_monthcompleted_workflowtype___workflows_dictionary,"{}:{}:{}".format(get_year_with_century(row[25]),get_month_as_decimal(row[25]),row[7]),row[0])

            workid = row[0]
            count += 1
        continue
        if workflow_file is not None:
            if row[0] != workid and workid != 0:
                workflow_file.close()
                workflow_file = None

        if workflow_file is None:
            workflow_file = open("/Users/kyle/Code/IEM-BIG-DATA/single_workflows/"+row[0]+".csv","w")
            workflow_writer = csv.writer(workflow_file,delimiter=',')

         # write value
        workflow_writer.writerow(row)
write_index(yearcompleted_workflowtype___workflows_dictionary,'workflows_by_year_and_type')
write_index(workflowtype___workflows_dictionary,'workflows_by_type')
