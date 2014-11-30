#!/usr/bin/python
import mwclient
import json
import re

# DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV
mediawiki_account_config = '/home/eric/.ssh/ebola-dev-robot.json'

mwaccount = json.load(open(mediawiki_account_config))

mwsite = mwclient.Site(mwaccount['site'], path=mwaccount['sitepath'])
mwsite.login(mwaccount['username'],mwaccount['password'])

for page in mwsite.pages:
    # page.page_title
    oldpagetext = page.text()
    fileprefix =  re.sub('[ /]','_',page.page_title)
    if '[[category:organizations]]' in oldpagetext or '[[category:locations]]' in oldpagetext or '[[category:people]]' in oldpagetext:
      print "Editing ", fileprefix, "\n\n\n"
      entity_graph = """
      <!-- entity_graph_begin -->
      <div id='entity_graph' file='%s'></div>
      <div id='entity_graph_menu'></div>
      <!-- entity_graph_end -->
      """ % fileprefix

      if "<!--entity_graph_begin-->" in oldpagetext: # Strip the old graph if it exists
        oldpagetext = re.sub(re.escape('<!--entity_graph_begin-->') + '.*' + re.escape('<!--entity_graph_end-->'),'',oldpagetext)

      newpagetext = entity_graph + oldpagetext

      #print newpagetext

      page.save(newpagetext, summary='subgraph append')
