#!/usr/bin/python
import sys
import json
import happybase

try:
    infile = open(sys.argv[1], 'r')
except IndexError:
    infile = sys.stdin
records = json.load(infile)

#for record in records:
    #print record["cleaned_text"]

connection = happybase.Connection('r102u25.xdata.data-tactics-corp.com')
connection.open()

#hbase shell>create 'ebola-wiki-scrape-v1', 'orig', 'image', 'file', 'inference'
table = connection.table('ebola-wiki-scrape-v1')
