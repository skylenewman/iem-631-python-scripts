#!/usr/bin/python
import csv
import json
import re
from datetime import datetime

datareader = None
my_list = []
def p(s):
    while len(s) < 10:
        s = s + " "
    return s
def add_to_list(v):
    if v not in my_list:
        my_list.append(v)

with open("/Users/kyle/Code/IEM-BIG-DATA/DIFFS.csv") as infile:
    datareader = csv.reader(infile)
    for r in datareader:
        add_to_list(r[0])


index_file = open("/Users/kyle/Code/IEM-BIG-DATA/i/all.csv","w")
for r in my_list:
    index_file.write(r)
    index_file.write('\n')
index_file.close()
