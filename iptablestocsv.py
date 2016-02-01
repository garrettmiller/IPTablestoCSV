#!/usr/bin/python
##############################################
#iptablestocsv.py
#2016 Garrett Miller
#Carnegie Mellon University
#
#Some code inspired by:
#Synce: http://codetwit.com/quick-python-to-parse-a-file-and-get-ips.html
#and Chriszuma: http://stackoverflow.com/questions/7679624/how-do-i-parse-lines-from-a-log-file
##############################################

#Imports
import sys
import re
import csv

#Get input from CLI
if sys.argv[1:]:
    print "File: %s" % (sys.argv[1])
    logfile = sys.argv[1]
    outfile = sys.argv[2]
else: #Or get it interactively
    logfile = raw_input("Please enter a path to an IPTables log file to parse, e.g /home/user/iptables.log: ")
    outfile = raw_input("Please enter a path for an output CSV file: ")

#Open CSV file for writing
fieldnames = ['IN', 'PHYSIN', 'OUT', 'PHYSOUT', 'SRC', 'DST', 'LEN', 'TOS', 'PREC', 
'TTL', 'ID', 'PROTO', 'SPT', 'DPT', 'WINDOW', 'RES', 'URGP']
writer = csv.DictWriter(open(outfile, "wb"), fieldnames=fieldnames, delimiter=',')
writer.writeheader()

#Open logfile for reading
try:
    file = open(logfile, "r")
except IOError, (errno, strerror):
    print "I/O Error(%s) : %s" % (errno, strerror)
pair_re = re.compile('([^ ]+)=([^ ]+)')  # Matches KEY=value pair
for line in file.readlines():
    line = line.rstrip()  # Removes final spaces and newlines
    data = dict(pair_re.findall(line))  # Fetches all the KEY=value pairs and puts them in a dictionary

    ################
    #Debug - print to see output, leave commented for faster running
    #print data
    ################

    try:  #Use a try block in case not all elements are always there
        writer.writerow({'IN': data['IN'], 'PHYSIN': data['PHYSIN'], 'OUT': data['OUT'], 'PHYSOUT': data['PHYSOUT'], 
       'SRC': data['SRC'], 'DST': data['DST'], 'LEN': data['LEN'], 'TOS': data['TOS'], 'PREC': data['PREC'], 
       'TTL': data['TTL'], 'ID': data['ID'], 'PROTO': data['PROTO'], 'SPT': data['SPT'], 'DPT': data['DPT'], 
       'WINDOW': data['WINDOW'], 'RES': data['RES'], 'URGP': data['URGP']})
    except KeyError:
        continue
#Close file
file.close()

