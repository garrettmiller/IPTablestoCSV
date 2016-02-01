#!/usr/bin/python
##############################################
#iptablestocsv-integers.py
#Converts IPTables logfiles to CSV data
#"-integers" adds column for IPs as integers.
#2016 Garrett Miller
#Carnegie Mellon University
#
#Some code inspired by:
#Synce: http://codetwit.com/quick-python-to-parse-a-file-and-get-ips.html
#and Chriszuma: http://stackoverflow.com/questions/7679624/how-do-i-parse-lines-from-a-log-file
##############################################

#Imports
import sys, re, csv

#Get input from CLI
if sys.argv[1:]:
    print "File: %s" % (sys.argv[1])
    logfile = sys.argv[1]
    outfile = sys.argv[2]
else: #Or get it interactively
    logfile = raw_input("Please enter a path to an IPTables log file to parse, e.g /home/user/iptables.log: ")
    outfile = raw_input("Please enter a path for an output CSV file: ")

#Open CSV file for writing
fieldnames = ['IN', 'PHYSIN', 'OUT', 'PHYSOUT', 'SRC','SRC-INT', 'DST', 'DST-INT',
 'LEN', 'TOS', 'PREC', 'TTL', 'ID', 'PROTO', 'SPT', 'DPT', 'WINDOW', 'RES', 'URGP']
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

    #Convert IP addresses to integers
    #Use a try block in case not all elements are always there
    try:  
        srcip = data['SRC']
    except KeyError:
        continue
    try:
        destip = data['DST']
    except KeyError:
        continue
    srcparts = srcip.split('.')
    destparts = destip.split('.')
    srcipint = (int(srcparts[0]) << 24) + (int(srcparts[1]) << 16) + (int(srcparts[2]) << 8) + int(srcparts[3])
    destipint = (int(destparts[0]) << 24) + (int(destparts[1]) << 16) + (int(destparts[2]) << 8) + int(destparts[3])

    ################
    #Debug - print to see output, leave commented for faster running
    #print data
    ################

    try:  #Use a try block in case not all elements are always there
        writer.writerow({'IN': data['IN'], 'PHYSIN': data['PHYSIN'], 'OUT': data['OUT'], 'PHYSOUT': data['PHYSOUT'], 
        'SRC': data['SRC'], 'SRC-INT': srcipint, 'DST': data['DST'], 'DST-INT': destipint, 'LEN': data['LEN'], 
        'TOS': data['TOS'], 'PREC': data['PREC'], 'TTL': data['TTL'], 'ID': data['ID'], 'PROTO': data['PROTO'], 
        'SPT': data['SPT'], 'DPT': data['DPT'], 'WINDOW': data['WINDOW'], 'RES': data['RES'], 'URGP': data['URGP']})
    except KeyError:
        continue
#Close file
file.close()

