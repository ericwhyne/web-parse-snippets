#!/usr/bin/python
import mwclient
import json
import re

mediawiki_account_config = '/home/eric/.ssh/ebola-robot.json'

mwaccount = json.load(open(mediawiki_account_config))

mwsite = mwclient.Site(mwaccount['site'], path=mwaccount['sitepath'])
mwsite.login(mwaccount['username'],mwaccount['password'])

for page in mwsite.pages:
    # page.page_title
    oldpagetext = page.text()
    fileprefix =  re.sub('[ /]','_',page.page_title)
    if '[[category:organizations]]' in oldpagetext or '[[category:locations]]' in oldpagetext or '[[category:people]]' in oldpagetext:
      print "Editing ", fileprefix
      entity_graph = """<div id='entity_graph' file='%s'></div>""" % fileprefix

      if "<div id='entity_graph'" in oldpagetext:
        entity_graph = "" # do something else, usually nothing
        print "Skipping ", fileprefix

      newpagetext = entity_graph + oldpagetext

      #print newpagetext

      page.save(newpagetext, summary='subgraph append')
