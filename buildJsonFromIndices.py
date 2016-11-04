#!/usr/bin/python
from datetime import datetime
import csv
# import sys
import json
import os
# import numpy
# from scipy import stats
# from pprint import pprint

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
        'duration':r[45]
    }
def print_list_stats(d):
    # Returns modal value and count of modal values
    a,b = stats.mode(d)
    hist, bin_edges = numpy.histogram(d,'auto')
    print ''
    # print d
    print "freq d: {} : {}".format(hist, bin_edges)
    print "mean  : {}".format(numpy.average(d))
    print "median: {}".format(numpy.median(d))
    print "mode  : {} : {}".format(a[0],b[0])
    print "range : {}".format(max(d) - min(d))
    print "std dv: {}".format(numpy.std(d))

def convert_to_int(d):
    if d is not None and d != '':
        try:
            # print datetime.strptime(d,"%d-%b-%y").total_seconds()
            print "d {}".format(d)
            print "e {}".format(datetime.strptime(d,"%d-%b-%y"))

            print "f {}".format(datetime.strptime(d,"%d-%b-%y").microsecond)
            print "g {}".format(datetime.strptime(d,"%d-%b-%y").microsecond/1000)
            d2 = datetime.strptime(d,"%d-%b-%y")
            epoch = datetime.strptime("01-JAN-70","%d-%b-%y")
            print epoch
            print "h {}".format(abs((d2-epoch).days))
            print "h {}".format(abs((d2-epoch)))
            # TODO: Just make this days

            # print time.mktime(d.datetime.strptime(compare_date.strftime("%d-%b-%y"), "%d-%b-%y").timetuple())
            # return time.mktime(struct)
            # return datetime.fromtimestamp(mktime(struct))
            # return datetime.strptime(d,"%d-%b-%y").total_seconds()
        except ValueError:
            return 0
    else:
        return 0

rootdir = "/Users/kyle/Code/IEM-BIG-DATA/i/"
for subdir, dirs, files in os.walk("/Users/kyle/Code/IEM-BIG-DATA/i/a.status_type/"):

    # LOOP THROUGH THE INDEX FILES IN THE DIRECTORY
    for f in files:
        # How many workflows are in each workflow?
        workflows_in_index = 0

        c_id_list = [] # [subworkflows][subworkflow][tasks][task][task_id]

        a_status_list = []
        b_status_list = []

        a_duration_list = []
        b_duration_list = []
        c_duration_list = []

        a_dateinit_list = []
        a_datecomp_list = []

        index_csv_file = open(os.path.join(subdir,f))
        index_csv_reader = csv.reader(index_csv_file)
        for r in index_csv_reader:
            workflows_in_index += 1

            # OPEN THE INDIVIDUAL WORKFLOW
            workflow_json = open("/Users/kyle/Code/IEM-BIG-DATA/w/"+r[0]+".json")
            data = json.load(workflow_json)

            a_status_list.append(int(data['status_cd']))
            a_duration_list.append(int(data['duration']))
            print convert_to_int(data['date_completed'])
            # a_dateinit_list.append(int(convert_to_int(data['date_initiated'])))
            # a_datecomp_list.append(int(convert_to_int(data['date_completed'])))
            task_count = 0
            for swf in data['subworkflows']:
                b_status_list.append(int(swf['status_cd']))
                b_duration_list.append(int(swf['duration']))
                # task_count += 1
                # print task_count
                for t in swf['tasks']:
                    c_id_list.append(int(t['task_id']))
                    if t['duration'] is not None and t['duration'] != '':
                        c_duration_list.append(int(t['duration']))

            # Read JSON
            # CLOSE WORKFLOW FILE
            workflow_json.close()
            # print data['id']
            # print swt_id_list
            # pause = raw_input("next:")

        # pause = raw_input("next:")
        # print_list_stats(a_dateinit_list)
        # print_list_stats(a_datecomp_list)

exit()
if None:
    for file in os.listdir("/Users/kyle/Code/IEM-BIG-DATA/w/"):
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
                workflow_dictionary['owner_id'] = r[35]
                workflow_dictionary['manager_id'] = r[38]
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
                    if swf['id'] == r[1] and 'tasks' in swf and swf['tasks'] is not None:
                        tmp = swf['tasks']
                        tmp.append(subworktask)
                        swf['tasks'] = tmp
            if swt_id is None or swt_id != r[2]:
                swt_id = r[2]
        csv_file.close()

        json_file = open("/Users/kyle/Code/IEM-BIG-DATA/w/"+jsonfile,'w')
        json.dump(workflow_dictionary,json_file)
        json_file.close()
