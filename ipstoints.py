#!/usr/bin/python
##############################################
#ipstoints.py
#Changes IP addresses in a CSV file to integers
#and then an index for PCA analysis.
#2016 Garrett Miller
#Carnegie Mellon University
###############################################

#Imports
import sys, re, csv

#Function to uniquify a list
def uniquify(seq):
    e = 0
    keys = {}
    for e in seq:
        keys[e] = 1
    return keys.keys()

#Declare empty lists for unique IP addresses
srclist=[]
destlist=[]

#Get input from CLI
if sys.argv[1:]:
    print "File: %s" % (sys.argv[1])
    csvfile = sys.argv[1]
    outfile = sys.argv[2]
else: #Or get it interactively
    csvfile = raw_input("Please enter a path to an CSV file to parse, e.g /home/user/iptables.csv: ")
    outfile = raw_input("Please enter a path for an output CSV file: ")

#Read file through for the first time
f = open(csvfile)
csv_f = csv.reader(f)
csv_f.next()
for row in csv_f:
    srcip = row[2]
    destip = row[3]

    srcparts = srcip.split('.')
    destparts = destip.split('.')

    srcipint = (int(srcparts[0]) << 24) + (int(srcparts[1]) << 16) + (int(srcparts[2]) << 8) + int(srcparts[3])
    destipint = (int(destparts[0]) << 24) + (int(destparts[1]) << 16) + (int(destparts[2]) << 8) + int(destparts[3])

    #Append IP ints to list
    srclist.append(srcipint)
    destlist.append(destipint)

#Uniquify our lists, then sort.
srclist = uniquify(srclist)
destlist = uniquify(destlist)
srclist.sort()
destlist.sort()

f.close()

#Read it again while writing to rewrite IPs with index ints
f = open(csvfile)
csv_f = csv.reader(f)
writer = csv.writer(open(outfile, 'w'))
writer.writerow(next(csv_f))
for row in csv_f:
    srcip = row[2]
    destip = row[3]

    srcparts = srcip.split('.')
    destparts = destip.split('.')

    srcipint = (int(srcparts[0]) << 24) + (int(srcparts[1]) << 16) + (int(srcparts[2]) << 8) + int(srcparts[3])
    destipint = (int(destparts[0]) << 24) + (int(destparts[1]) << 16) + (int(destparts[2]) << 8) + int(destparts[3])

    #Set integer to index of its location in list
    srcipint = srclist.index(srcipint)
    destipint = destlist.index(destipint)

    row[2] = srcipint
    row[3] = destipint

    writer.writerow(row)
