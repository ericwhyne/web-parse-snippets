#!/usr/bin/python
import json
import sys
import re

if len(sys.argv) != 5:
  print "Usage: ", sys.argv[0], " infile.json data/graph_data/ 2 minlinks-2"
  sys.exit(0)

filename = sys.argv[1]
subgraphdir = sys.argv[2]
min_number_of_shared_citations = int(sys.argv[3])
file_postfix = sys.argv[4]


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

for i, ival in enumerate(graph['nodes']):
  sub_graph = {}
  sub_graph['nodes'] = []
  sub_graph['links'] = []
  sub_graph_filename = subgraphdir + re.sub('[ /]','_',ival['name']) + '-' + file_postfix + '.json'
  #sub_graph_htm = subtestdir + re.sub('[ /]','_',ival['name']) + ".htm"
  pagename = re.sub(' ','_',ival['name'])
  num_urls = len(ival['urls'])
  sub_graph['nodes'].append({"name":ival['name'],"group":ival['group'],"pagename":pagename,"urls":ival['urls'],"num_urls":num_urls})

  # find links between our graph's element and everything else.
  for j, jval in enumerate(graph['nodes']):
    url_intersection = list(set(ival['urls']) & set(jval['urls']))
    if len(url_intersection) >= min_number_of_shared_citations and ival['name'] != jval['name']:
      num_urls = len(jval['urls'])
      sub_graph['nodes'].append({"name":jval['name'],"group":jval['group'],"pagename":re.sub(' ','_',jval['name']),"urls":jval['urls'], "num_urls":num_urls, "intersection":url_intersection, "url":'/' + re.sub('[ /]','_',jval['name'])})
      sub_graph['links'].append({"source":0,"target":len(sub_graph['nodes']) - 1,"value":len(url_intersection)})

  # find links between added nodes
  for k, kval in enumerate(sub_graph['nodes']):
    for l, lval in enumerate(sub_graph['nodes']):
      url_intersection = list(set(kval['urls']) & set(lval['urls']))
      if len(url_intersection) >= min_number_of_shared_citations and kval['name'] != lval['name']:
        #print kval['name']
        sub_graph['links'].append({"source":k,"target":l,"value":len(url_intersection)})

  json.dump(sub_graph, open(sub_graph_filename,'w'))

#  html_file = open(sub_graph_htm, 'w')
#  div_file = re.sub('[ /]','_',ival['name'])
  html = '''
  <html>
  <div id='entity_graph' file='%s'></div>
  <div id='entity_graph_menu'></div>

  <script src="d3.v3.min.js"></script>
  <script src="graph_make.js"></script>
  <link rel="stylesheet" href="graph_style.css">
  </html>
  '''# % div_file
  #html_file.write(html.encode('utf-8'))




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
