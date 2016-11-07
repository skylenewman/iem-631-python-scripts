#!/usr/bin/python
import csv
import sys
import json
import os
from pprint import pprint

datareader = None
workid = 0

def add_to_list(v,l):
    if v not in l:
        l.append(v)

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

def get_subworktask(r):
    return {
        'task_id':r[2],
        'title':r[8],
        'status_cd':r[15],
        'status':r[46],
        'date_due_min':r[18],
        'date_due_max':r[21],
        'date_ready':r[27],
        'date_due_duration':r[44],
        'duration':r[45],
        'performer':get_user_dict(r[37]),
        'owner':get_user_dict(r[36]),
        'manager':get_user_dict(r[39])
    }

user_group_dict = {}
with open("/Users/kyle/Code/IEM-BIG-DATA/IEM-USERS-GROUPS.csv") as infile:
    datareader = csv.reader(infile)
    for r in datareader:

        user_group_dict[r[0]] = {
            'type_cd':r[1],
            'group_cd':r[2],
            'deleted_cd':r[3],
            'type':'user' if r[1] == '0' else 'group',
            'status':'active' if r[3] == '0' else 'inactive'
        }
def get_user_dict(i):
    if i is not None and i != '' and i in user_group_dict:
        return {
            'id':i,
            'type_cd':user_group_dict[i]['type_cd'],
            'group_cd':user_group_dict[i]['group_cd'],
            'deleted_cd':user_group_dict[i]['deleted_cd'],
            'type':user_group_dict[i]['type'],
            'status':user_group_dict[i]['status'],
        }
    elif i == '1000':
        return {
            'type_cd':'2',
            'group_cd':'1',
            'deleted_cd':'1',
            'type':'system automation',
            'status':'active',
        }
    else:
        return i
for file in os.listdir("/Users/kyle/Code/IEM-BIG-DATA/w/"):
    if file.endswith("csv"):
        jsonfile = file.replace("csv","json")

        workflow_dictionary = {}
        subwork_dictionary = {}
        w_id = None
        sw_id = None
        swt_id = None
        csv_file = open("/Users/kyle/Code/IEM-BIG-DATA/w/"+file)
        datareader = csv.reader(csv_file)
        for r in datareader:
            if w_id is None:
                w_id = r[0]
                workflow_dictionary['id'] = w_id
                workflow_dictionary['status_cd'] = r[11]
                workflow_dictionary['status'] = r[12]
                workflow_dictionary['date_due_min'] = r[16]
                workflow_dictionary['date_due_max'] = r[19]
                workflow_dictionary['date_initiated'] = r[22]
                workflow_dictionary['date_completed'] = r[24]
                workflow_dictionary['owner'] = get_user_dict(r[35])
                workflow_dictionary['manager'] = get_user_dict(r[38])
                workflow_dictionary['date_due_duration'] = r[40]
                workflow_dictionary['duration'] = r[41]
                workflow_dictionary['title'] = r[8]

            if r[1] not in subwork_dictionary:
                sw_id = r[1]
                subworktask = get_subworktask(r)
                subwork_dictionary[r[1]] = [subworktask]
                subworkflow = {
                    'subworkflow_id':r[1],
                    'return_id':r[6],
                    'title':r[7],
                    'status_cd':r[13],
                    'status':r[14],
                    'date_due_min':r[17],
                    'date_due_max':r[20],
                    'date_initiated':r[23],
                    'date_completed':r[25],
                    'date_due_duration':r[42],
                    'duration':r[43],
                    'tasks':[subworktask]

                }
                if 'subworkflows' in workflow_dictionary:
                    tmp = workflow_dictionary['subworkflows']
                    tmp.append(subworkflow)
                    workflow_dictionary['subworkflows'] = tmp
                else:
                    workflow_dictionary['subworkflows'] = [subworkflow]
            else:
                subworktask = get_subworktask(r)
                if r[1] in subwork_dictionary:
                    tmp = subwork_dictionary[r[1]]
                    tmp.append(subworktask)
                    subwork_dictionary[r[1]] = tmp
                else:
                    subwork_dictionary[r[1]] = [subworktask]
                for swf in workflow_dictionary['subworkflows']:
                    if 'subworkflow_id' in swf and swf['subworkflow_id'] == r[1] and 'tasks' in swf and swf['tasks'] is not None:
                        tmp = swf['tasks']
                        tmp.append(subworktask)
                        swf['tasks'] = tmp
            if swt_id is None or swt_id != r[2]:
                swt_id = r[2]
        csv_file.close()


        json_file = open("/Users/kyle/Code/IEM-BIG-DATA/ww/"+jsonfile,'w')
        json.dump(workflow_dictionary,json_file)
        json_file.close()
