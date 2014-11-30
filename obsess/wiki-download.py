#!/usr/bin/python
import mwclient
import json
import obsess
import datetime
import sys

today = datetime.date.isoformat(datetime.datetime.now())

if len(sys.argv) != 3:
  print "Usage: ", sys.argv[0], " /home/eric/.ssh/ebola-dev-robot.json outfile.json"

mediawiki_account_config = sys.argv[1]
data_logfilename = sys.argv[2]

mwaccount = json.load(open(mediawiki_account_config))

mwsite = mwclient.Site(mwaccount['site'], path=mwaccount['sitepath'])
mwsite.login(mwaccount['username'],mwaccount['password'])

for page in mwsite.pages:
    record = {}
    record['title'] = page.page_title
    record['text'] = page.text()
    #print record
    obsess.log_data(record, data_logfilename)
