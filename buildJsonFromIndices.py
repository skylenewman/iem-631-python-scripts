#!/usr/bin/python
from datetime import datetime, timedelta
import csv
import sys
import json
import os
import numpy
from scipy import stats
from pprint import pprint
import codecs

datareader = None
workid = 0

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

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
def get_freq_d(d,bins=5):
    if d is not None and len(d) > 0:
        hist, bin_edges = numpy.histogram(d,bins)
        # print "freq d1  : {} : {}".format(hist, bin_edges)
        edges = []
        for e in bin_edges:
            # print "         {} :: {}".format(e,int(e))
            if int(e) not in edges:
                if int(e) > 0:
                    edges.append(int(e))
                else:
                    if 0 not in edges:
                        edges.append(0)
        e_hist,e_bin_edges = numpy.histogram(d,edges)
        json_hist = {}
        for x in range(0,len(e_hist)-1):
            json_hist[x] = {
                'count':e_hist[x],
                'lower':e_bin_edges[x],
                'upper':e_bin_edges[x+1]
            }
        # return {
        #     'numbers':e_hist,
        #     'bin_edges':e_bin_edges
        # }
        return json_hist
    else:
        print "d is {}".format(d)

def get_stats_dict(d):
    l = []
    for k in d:
        l.append(d[k])
    return get_stats(l)

def get_percentage(per,whole):
    return round(float(float(per)/float(whole))*100,2)
def get_stats(d):
    if d is not None and len(d) > 0:
        cont = False
        for r in d:
            if r != 0:
                cont = True
                break
        if cont == False:
            return None
        return_dict = {}
        return_dict['total_count'] = len(d)
        return_dict['freq'] = {}
        return_dict['freq']['5'] = get_freq_d(d)
        return_dict['freq']['10'] = get_freq_d(d,10)
        return_dict['freq']['20'] = get_freq_d(d,20)
        return_dict['mean'] = round(numpy.average(d),2)
        return_dict['median'] = int(numpy.median(d))
        mode_m,mode_c = stats.mode(d)
        return_dict['mode'] = {
            'value':mode_m[0],
            'count':mode_c[0],
            'percent_whole':get_percentage(mode_c,len(d))
        }
        return_dict['range'] = int(max(d) - min(d))
        return_dict['std_dev'] = round(numpy.std(d),2)
        return_dict['percentiles'] = {
            '5':round(numpy.percentile(d,5),2),
            '10':round(numpy.percentile(d,10),2),
            '15':round(numpy.percentile(d,15),2),
            '20':round(numpy.percentile(d,20),2),
            '25':round(numpy.percentile(d,25),2),
            '30':round(numpy.percentile(d,30),2),
            '35':round(numpy.percentile(d,35),2),
            '40':round(numpy.percentile(d,40),2),
            '45':round(numpy.percentile(d,45),2),
            '50':round(numpy.percentile(d,50),2),
            '55':round(numpy.percentile(d,55),2),
            '60':round(numpy.percentile(d,60),2),
            '65':round(numpy.percentile(d,65),2),
            '70':round(numpy.percentile(d,70),2),
            '75':round(numpy.percentile(d,75),2),
            '80':round(numpy.percentile(d,80),2),
            '85':round(numpy.percentile(d,85),2),
            '90':round(numpy.percentile(d,90),2),
            '95':round(numpy.percentile(d,95),2),
            '100':round(numpy.percentile(d,100),2)
        }
        unique, counts = numpy.unique(d, return_counts=True)
        ind_counts = dict(zip(unique, counts))
        return_dict['counts'] = {}
        for k in ind_counts:
            pct = get_percentage(ind_counts[k],len(d))
            return_dict['counts'][k] = {
                'count':ind_counts[k],
                'percentage':pct
            }
        return return_dict
    else:
        return None

def print_list_stats(d):
    if d is not None and len(d) > 0:
        # Returns modal value and count of modal values
        a,b = stats.mode(d)
        print ''
        # print d
        print ''
        print "size     : {}".format(len(d))
        print "mean     : {}".format(numpy.average(d))
        print "mean     : {}".format(numpy.mean(d))
        print "median   : {}".format(numpy.median(d))
        print "mode     : {} : {}".format(a[0],b[0])
        print "range    : {}".format(max(d) - min(d))
        print "std dv   : {}".format(numpy.std(d))
        print "variance : {}".format(numpy.var(d))
        print "bincount : {}".format(numpy.bincount(d))
        print "10 pcnt  : {}".format(numpy.percentile(d,10))
        print "50 pcnt  : {}".format(numpy.percentile(d,50))
        print "90 pcnt  : {}".format(numpy.percentile(d,90))
        print "freq d   : {}".format(get_freq_d(d))

def convert_to_int(d):
    if d is not None and d != '':
        try:
            d = datetime.strptime(d,"%d-%b-%y")
            epoch = datetime.strptime("01-JAN-70","%d-%b-%y")
            return abs((d-epoch).days)
        except ValueError:
            return -1
    else:
        return -1

def get_month_as_decimal(d):
    if d is not None and d != '':
        try:
            d = datetime.strptime(d,"%d-%b-%y")
            return int(d.strftime("%m"))
        except ValueError:
            return -1
    else:
        return -1

def get_year_with_century(d):
    if d is not None and d != '':
        try:
            d = datetime.strptime(d,"%d-%b-%y")
            return int(d.strftime("%Y"))
        except ValueError:
            return -1
    else:
        return -1

def days_between(d1,d2):
    if d1 is not None and d1 != '':
        try:
            d1 = datetime.strptime(d1,"%d-%b-%y")
            if d2 is None or d2 == '':
                d2 = now
            else:
                d2 = datetime.strptime(d2,"%d-%b-%y")
            return int(abs((d2-d1).days))
        except ValueError:
            return -1

def get_day_of_year(d):
    if d is not None and d != '':
        try:
            d = datetime.strptime(d,"%d-%b-%y")
            return int(d.strftime("%j"))
        except ValueError:
            return -1
    else:
        return -1

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

# def serial_date_to_string(srl_no):
#     dt = datetime.datetime(1970,1,1,0,0)
#     td = datetime.timedelta(srl_no - 1)
#     new_date = dt + td
#     return new_date.strftime("%Y-%m-%d")

def log_workflowtype(d,l,v):
    if v not in d:
        d[v] = len(d)
    l.append(d[v])

rootdir = "/Users/kyle/Code/IEM-BIG-DATA/i/"
for subdir, dirs, files in os.walk("/Users/kyle/Code/IEM-BIG-DATA/i/"):
    index_json = {}
    # LOOP THROUGH THE INDEX FILES IN THE DIRECTORY
    for f in files:
        # How many workflows are in each workflow?
        workflows_in_index = 0

        c_id_list = []

        a_status_list = []
        b_status_list = []
        c_status_list = []

        a_duration_list = []
        b_duration_list = []
        c_duration_list = []

        a_dateinit_list = []
        a_datecomp_list = []

        a_monthinit_list = []
        a_monthcomp_list = []

        a_yearinit_list = []
        a_yearcomp_list = []

        a_dayofyear_init_list = []
        a_dayofyear_comp_list = []

        number_subworkflow_list = []
        number_subworktask_list = []

        b_duedate_duration_list = []

        j_worked_list = []

        a_owner_user_list = []
        a_manager_user_list = []
        a_owner_group_list = []
        a_manager_group_list = []


        a_completed_workflows = []
        a_incomplete_workflows = []

        a_workflowtype___workflows_dict = {}
        a_workflowtype_list = []
        a_workflowtype_dict = {}

        a_owner_type_list = []
        a_manager_type_list = []
        c_performer_user_list = []
        c_performer_group_list = []
        c_performer_type_list = []
        c_owner_user_list = []
        c_owner_group_list = []
        c_owner_type_list = []
        c_manager_user_list = []
        c_manager_group_list = []
        c_manager_type_list = []

        index_csv_file = open(os.path.join(subdir,f))
        index_csv_reader = csv.reader(index_csv_file)
        for r in index_csv_reader:
            workflows_in_index += 1

            fname = "/Users/kyle/Code/IEM-BIG-DATA/ww/"+r[0]+".json"
            cont = os.path.isfile(fname)
            if cont != True:
                print "{} was not a file".format(fname)
                continue
            # OPEN THE INDIVIDUAL WORKFLOW
            workflow_json = open(fname)
            data = json.load(workflow_json)

            a_status_list.append(int(data['status_cd']))
            a_duration_list.append(int(data['duration']))

            add_to_dict_list(a_workflowtype___workflows_dict,data['title'],data['id'])


            log_workflowtype(a_workflowtype_dict,a_workflowtype_list,data['title'])

            if data['owner'] is not None:
                if isinstance(data['owner'],dict):
                    if data['owner']['type'] == 'user':
                        if data['owner']['id'] is not None and int(data['owner']['id']) != -1:
                            a_owner_user_list.append(int(data['owner']['id']))
                        if data['owner']['group_cd'] is not None and int(data['owner']['group_cd']) > 0:
                            a_owner_group_list.append(int(data['owner']['group_cd']))
                        # print data['manager']['type_cd']
                        if data['manager'] is not None:

                            try:
                                if data['manager']['type_cd'] is not None:
                                    # print data
                                    tc = data['manager']['type_cd']
                                    tci = int(tc)
                                    if tci != -1:
                                        a_owner_type_list.append(int(data['manager']['type_cd']))
                            except TypeError:
                                pass

                    else:
                        if data['owner']['id'] is not None and int(data['owner']['id']) != -1:
                            a_owner_group_list.append(int(data['owner']['id']))
                        if data['manager']['type_cd'] is not None and int(data['manager']['type_cd']) != -1:
                            a_owner_type_list.append(int(data['manager']['type_cd']))

            if data['manager'] is not None:
                if isinstance(data['manager'],dict):
                    if data['manager']['type'] == 'user':
                        if data['manager']['id'] is not None and int(data['manager']['id']) != -1:
                            a_manager_user_list.append(int(data['manager']['id']))
                        if data['manager']['group_cd'] is not None and int(data['manager']['group_cd']) > 0:
                            a_manager_group_list.append(int(data['manager']['group_cd']))
                        if data['manager']['type_cd'] is not None and int(data['manager']['type_cd']) != -1:
                            a_manager_type_list.append(int(data['manager']['type_cd']))
                    else:
                        if data['manager']['id'] is not None and int(data['manager']['id']) != -1:
                            a_manager_group_list.append(int(data['manager']['id']))
                        if data['manager']['type_cd'] is not None and int(data['manager']['type_cd']) != -1:
                            a_manager_type_list.append(int(data['manager']['type_cd']))

            date_initiated = convert_to_int(data['date_initiated'])
            if date_initiated is not None and date_initiated != -1:
                a_dateinit_list.append(date_initiated)
            date_completed = convert_to_int(data['date_completed'])
            if date_completed is not None and date_completed != -1:
                a_datecomp_list.append(date_completed)

            monthinit = get_month_as_decimal(data['date_initiated'])
            if monthinit is not None and monthinit != '' and monthinit != -1:
                a_monthinit_list.append(monthinit)

            monthcomp = get_month_as_decimal(data['date_completed'])
            if monthcomp is not None and monthcomp != '' and monthcomp != -1:
                a_monthcomp_list.append(monthcomp)

            yearinit = get_year_with_century(data['date_initiated'])
            if yearinit is not None and yearinit != '' and yearinit != -1:
                a_yearinit_list.append(yearinit)

            yearcomp = get_year_with_century(data['date_completed'])
            if yearcomp is not None and yearcomp != '' and yearcomp != -1:
                a_yearcomp_list.append(yearcomp)

            dayofyear_init = get_day_of_year(data['date_initiated'])
            if dayofyear_init is not None and dayofyear_init != '' and dayofyear_init != -1:
                a_dayofyear_init_list.append(dayofyear_init)

            dayofyear_comp = get_day_of_year(data['date_completed'])
            if dayofyear_comp is not None and dayofyear_comp != '' and dayofyear_comp != -1:
                a_dayofyear_comp_list.append(dayofyear_comp)

            if data['date_completed'] is None or data['date_completed'] == '':
                a_incomplete_workflows.append(data['id'])
            else:
                a_completed_workflows.append(data['id'])

            j_init = -1
            j_comp = -1
            if dayofyear_init is not None and dayofyear_init != '':
                j_init = int(float(dayofyear_init))
            if dayofyear_comp is not None and dayofyear_comp != '':
                j_comp = int(float(dayofyear_comp))
            if j_init != -1 and j_comp != -1:
                if j_init < j_comp:
                    for i in range(j_init,j_comp):
                        j_worked_list.append(i)
                else:
                    for i in range(j_init,366):
                        j_worked_list.append(i)
                    for i in range(0,j_comp):
                        j_worked_list.append(i)

            # for i in range(int(dayofyear_init),int(dayofyear_comp)):
                # print i
            # dayofyear_heat_list.append(x)

            subworkflow_count = 0
            for swf in data['subworkflows']:
                subworkflow_count += 1
                b_status_list.append(int(swf['status_cd']))
                # b_duedate_duration_list
                try:
                    b_duration_list.append(int(swf['duration']))
                except ValueError:
                    pass
                task_count = 0

                # LOOP THROUGH
                for t in swf['tasks']:
                    task_count += 1
                    c_id_list.append(int(t['task_id']))
                    if t['duration'] is not None and t['duration'] != '':
                        c_duration_list.append(int(t['duration']))
                    c_status_list.append(int(t['status_cd']))

                    if t['manager'] is not None:
                        if isinstance(t['manager'],dict):
                            if t['manager']['type'] == 'user':
                                c_manager_user_list.append(int(t['manager']['id']))
                                c_manager_group_list.append(int(t['manager']['group_cd']))
                                c_manager_type_list.append(int(t['manager']['type_cd']))
                            else:
                                c_manager_group_list.append(int(t['manager']['id']))
                                c_manager_type_list.append(int(t['manager']['type_cd']))

                    if t['owner'] is not None:
                        if isinstance(t['owner'],dict):
                            if t['owner']['type'] == 'user':
                                c_owner_user_list.append(int(t['owner']['id']))
                                c_owner_group_list.append(int(t['owner']['group_cd']))
                                c_owner_type_list.append(int(t['owner']['type_cd']))
                            else:
                                c_owner_group_list.append(int(t['owner']['id']))
                                c_owner_type_list.append(int(t['owner']['type_cd']))

                    if t['performer'] is not None:
                        if isinstance(t['performer'],dict):
                            if t['performer']['type'] == 'user':
                                c_performer_user_list.append(int(t['performer']['id']))
                                c_performer_group_list.append(int(t['performer']['group_cd']))
                                c_performer_type_list.append(int(t['performer']['type_cd']))
                            else:
                                c_performer_group_list.append(int(t['performer']['id']))
                                c_performer_type_list.append(int(t['performer']['type_cd']))

                # end for t in swf['tasks']:

                number_subworktask_list.append(task_count)
            # end for swf in data['subworkflows']:

            number_subworkflow_list.append(subworkflow_count)

            workflow_json.close()
        #
        # end for r in index_csv_reader:
        #

        my_json = {
            'workflows_number':workflows_in_index,
            'completed_workflows':{
                'count':len(a_completed_workflows)
            },
            'incomplete_workflows':{
                'count':len(a_incomplete_workflows)
            }
        }

        j_worked_list_stats = get_stats(j_worked_list)
        if j_worked_list_stats is not None and len(j_worked_list_stats) > 0:
            my_json['j_worked_list'] = j_worked_list_stats


        number_subworkflow_list_stats = get_stats(number_subworkflow_list)
        if number_subworkflow_list_stats is not None and len(number_subworkflow_list_stats) > 0:
            my_json['number_subworkflow_list'] = number_subworkflow_list_stats

        number_subworktask_list_stats = get_stats(number_subworktask_list)
        if number_subworktask_list_stats is not None and len(number_subworktask_list_stats) > 0:
            my_json['number_subworktask_list'] = number_subworktask_list_stats

        a_status_list_stats = get_stats(a_status_list)
        if a_status_list_stats is not None and len(a_status_list_stats) > 0:
            my_json['workflow_status_list'] = a_status_list_stats

        b_status_list_stats = get_stats(b_status_list)
        if b_status_list_stats is not None and len(b_status_list_stats) > 0:
            my_json['subworkflow_status_list'] = b_status_list_stats

        c_status_list_stats = get_stats(c_status_list)
        if c_status_list_stats is not None and len(c_status_list_stats) > 0:
            my_json['subworktask_status_list'] = c_status_list_stats

        c_id_list_stats = get_stats(c_id_list)
        if c_id_list_stats is not None and len(c_id_list_stats) > 0:
            my_json['subworktask_id_list'] = c_id_list_stats

        a_duration_list_stats = get_stats(a_duration_list)
        if a_duration_list_stats is not None and len(a_duration_list_stats) > 0:
            my_json['workflow_duration_list'] = a_duration_list_stats

        b_duration_list_stats = get_stats(b_duration_list)
        if b_duration_list_stats is not None and len(b_duration_list_stats) > 0:
            my_json['subworkflow_duration_list'] = b_duration_list_stats

        c_duration_list_stats = get_stats(c_duration_list)
        if c_duration_list_stats is not None and len(c_duration_list_stats) > 0:
            my_json['subworktask_duration_list'] = c_duration_list_stats

        a_monthinit_list_stats = get_stats(a_monthinit_list)
        if a_monthinit_list_stats is not None and len(a_monthinit_list_stats) > 0:
            my_json['a_monthinit_list'] = a_monthinit_list_stats

        a_monthcomp_list_stats = get_stats(a_monthcomp_list)
        if a_monthcomp_list_stats is not None and len(a_monthcomp_list_stats) > 0:
            my_json['a_monthcomp_list'] = a_monthcomp_list_stats

        a_dateinit_list_stats = get_stats(a_dateinit_list)
        if a_dateinit_list_stats is not None and len(a_dateinit_list_stats) > 0:
            my_json['a_dateinit_list'] = a_dateinit_list_stats

        a_datecomp_list_stats = get_stats(a_datecomp_list)
        if a_datecomp_list_stats is not None and len(a_datecomp_list_stats) > 0:
            my_json['a_datecomp_list'] = a_datecomp_list_stats

        a_yearinit_list_stats = get_stats(a_yearinit_list)
        if a_yearinit_list_stats is not None and len(a_yearinit_list_stats) > 0:
            my_json['a_yearinit_list'] = a_yearinit_list_stats

        a_yearcomp_list_stats = get_stats(a_yearcomp_list)
        if a_yearcomp_list_stats is not None and len(a_yearcomp_list_stats) > 0:
            my_json['a_yearcomp_list'] = a_yearcomp_list_stats

        a_dayofyear_comp_list_stats = get_stats(a_dayofyear_comp_list)
        if a_dayofyear_comp_list_stats is not None and len(a_dayofyear_comp_list_stats) > 0:
            my_json['a_dayofyear_comp_list'] = a_dayofyear_comp_list_stats

        a_dayofyear_init_list_stats = get_stats(a_dayofyear_init_list)
        if a_dayofyear_init_list_stats is not None and len(a_dayofyear_init_list_stats) > 0:
            my_json['a_dayofyear_init_list'] = a_dayofyear_init_list_stats

        b_duedate_duration_list_stats = get_stats(b_duedate_duration_list)
        if b_duedate_duration_list_stats is not None and len(b_duedate_duration_list_stats) > 0:
            my_json['b_duedate_duration_list'] = b_duedate_duration_list_stats

        a_owner_user_list_stats = get_stats(a_owner_user_list)
        if a_owner_user_list_stats is not None and len(a_owner_user_list_stats) > 0:
            my_json['a_owner_user_list'] = a_owner_user_list_stats

        a_manager_user_list_stats = get_stats(a_manager_user_list)
        if a_manager_user_list_stats is not None and len(a_manager_user_list_stats) > 0:
            my_json['a_manager_user_list'] = a_manager_user_list_stats

        a_owner_group_list_stats = get_stats(a_owner_group_list)
        if a_owner_group_list_stats is not None and len(a_owner_group_list_stats) > 0:
            my_json['a_owner_group_list'] = a_owner_group_list_stats

        a_manager_group_list_stats = get_stats(a_manager_group_list)
        if a_manager_group_list_stats is not None and len(a_manager_group_list_stats) > 0:
            my_json['a_manager_group_list'] = a_manager_group_list_stats

        a_owner_type_list_stats = get_stats(a_owner_type_list)
        if a_owner_type_list_stats is not None and len(a_owner_type_list_stats) > 0:
            my_json['a_owner_type_list'] = a_owner_type_list_stats

        a_manager_type_list_stats = get_stats(a_manager_type_list)
        if a_manager_type_list_stats is not None and len(a_manager_type_list_stats) > 0:
            my_json['a_manager_type_list'] = a_manager_type_list_stats

        c_performer_user_list_stats = get_stats(c_performer_user_list)
        if c_performer_user_list_stats is not None and len(c_performer_user_list_stats) > 0:
            my_json['c_performer_user_list'] = c_performer_user_list_stats

        c_performer_group_list_stats = get_stats(c_performer_group_list)
        if c_performer_group_list_stats is not None and len(c_performer_group_list_stats) > 0:
            my_json['c_performer_group_list'] = c_performer_group_list_stats

        c_performer_type_list_stats = get_stats(c_performer_type_list)
        if c_performer_type_list_stats is not None and len(c_performer_type_list_stats) > 0:
            my_json['c_performer_type_list'] = c_performer_type_list_stats

        c_owner_user_list_stats = get_stats(c_owner_user_list)
        if c_owner_user_list_stats is not None and len(c_owner_user_list_stats) > 0:
            my_json['c_owner_user_list'] = c_owner_user_list_stats

        c_owner_group_list_stats = get_stats(c_owner_group_list)
        if c_owner_group_list_stats is not None and len(c_owner_group_list_stats) > 0:
            my_json['c_owner_group_list'] = c_owner_group_list_stats

        c_owner_type_list_stats = get_stats(c_owner_type_list)
        if c_owner_type_list_stats is not None and len(c_owner_type_list_stats) > 0:
            my_json['c_owner_type_list'] = c_owner_type_list_stats

        c_manager_user_list_stats = get_stats(c_manager_user_list)
        if c_manager_user_list_stats is not None and len(c_manager_user_list_stats) > 0:
            my_json['c_manager_user_list'] = c_manager_user_list_stats

        c_manager_group_list_stats = get_stats(c_manager_group_list)
        if c_manager_group_list_stats is not None and len(c_manager_group_list_stats) > 0:
            my_json['c_manager_group_list'] = c_manager_group_list_stats

        c_manager_type_list_stats = get_stats(c_manager_type_list)
        if c_manager_type_list_stats is not None and len(c_manager_type_list_stats) > 0:
            my_json['c_manager_type_list'] = c_manager_type_list_stats

        # print my_json
        # print ''
        # print ''
        # print '###'
        # print ''
        # print my_json
        # continue
        last_path = os.path.basename(os.path.normpath(subdir))
        json_file_name = f.replace(".csv",".json")
        dict_key = f.replace(".csv","")
        directory = "/Users/kyle/Code/IEM-BIG-DATA/ij/"
        if json_file_name != 'all.json':
            directory = directory + last_path + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        print "Writing {}".format(directory + json_file_name)
        full_individual_json_path = directory + json_file_name
        # individual_json_file_no_lists = open(full_individual_json_path,"w")
        json.dump(my_json, codecs.open(full_individual_json_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
        index_json[dict_key] = my_json
    if json_file_name != 'all.json':
        last_path = os.path.basename(os.path.normpath(subdir))
        directory = "/Users/kyle/Code/IEM-BIG-DATA/ij/" + last_path + "/index.json"
        json.dump(index_json, codecs.open(directory , 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
        # json.dump(my_json,individual_json_file_no_lists)
        # individual_json_file_no_lists.close()
        #
        # unique, counts = numpy.unique(j_worked_list, return_counts=True)
        # ind_counts =  dict(zip(unique, counts))
        # print get_stats_dict(ind_counts)


        # my_json['completed_workflows']['list'] = a_completed_workflows
        # my_json['incomplete_workflows']['list'] = a_incomplete_workflows

        #
        # a_workflowtype___workflows_dict = {}
        # a_workflowtype_list = []
        # a_workflowtype_dict
        #
