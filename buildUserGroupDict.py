#!/usr/bin/python
import csv
import json
import re
from datetime import datetime

datareader = None

randomuser_dict = {}
with open('/Users/kyle/Code/IEM-BIG-DATA/randomuser.json') as random_user_file:
    randomuser_dict = json.load(random_user_file)

# group_name_list = []
# with open('/Users/kyle/Code/IEM-BIG-DATA/group_names.csv') as group_names_file:
#     datareader = csv.reader(group_names_file)
#     for r in datareader:
#         if len(r) > 0 and r[0] is not None and r[0] != '':
#             s = r[0]
#             s = s.strip()
#             t = s.replace(";","")
#             group_name_list.append(t)

user_group_dict = {}

# "ID","TYPE","GROUPID","DELETED"
count = 0
group_count = 0

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
        count != 1
        if r[1] == '1':
            print r[1]
            group_count += 1
# print user_group_dict[5703195]
# print user_group_dict

print group_count
