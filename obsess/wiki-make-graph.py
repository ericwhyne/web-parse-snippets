#!/usr/bin/python
import json
import sys
import re


filename = sys.argv[1]
logfile = open(filename, 'r')
records = json.load(logfile)

graph = {}
graph['nodes'] = []
graph['links'] = []
for record in records:
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', record['text'])
    if '[[category:organizations]]' in record['text']:
      graph['nodes'].append({"name":record['title'],"group":"1","urls":urls})
    if '[[category:locations]]' in record['text']:
      graph['nodes'].append({"name":record['title'],"group":"2","urls":urls})
    if '[[category:people]]' in record['text']:
      graph['nodes'].append({"name":record['title'],"group":"3","urls":urls})
    #for url in urls:
    #  print url
for i, ival in enumerate(graph['nodes']):
  for j, jval in enumerate(graph['nodes']):
    url_intersection = list(set(ival['urls']) & set(jval['urls']))
    if len(url_intersection) > 0:
      graph['links'].append({"source":i,"target":j,"value":len(url_intersection)})
    #print ival['name'], " ", jval['name'], " ", str(len(url_intersection))
for node in graph['nodes']:
  del node['urls']

print json.dumps(graph)

datastruct = '''
{
  "nodes":[
    {"name":"Myriel","group":1},
    {"name":"Napoleon","group":1},
    {"name":"Mlle.Baptistine","group":1}
    ],
  "links":[
    {"source":1,"target":0,"value":1},
    {"source":2,"target":0,"value":8},
    {"source":3,"target":0,"value":10}
    ]
}
'''
