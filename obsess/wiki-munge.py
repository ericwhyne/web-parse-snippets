#!/usr/bin/python
# coding=utf-8
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
#      print "Editing ", fileprefix
      # * [http://reddit.com/r/ebola/comments/2n1jyn/un_news_ebola_ban_hopeful_of_outbreaks_end_by/ Discus on Reddit]
      # * [http://reddit.com/r/EbolaGooglers/comments/2ji2fj/ebola_transmission_can_occur_from_sleeping_on_the/ Discus on Reddit]

      if u"�" in oldpagetext:
        print "found special on ", fileprefix
        newpagetext = re.sub(u"�",'',oldpagetext)
        print newpagetext
        page.save(newpagetext, summary='munged')
