#!/usr/bin/python
import mwclient
import json
import obsess
import datetime

today = datetime.date.isoformat(datetime.datetime.now())

mediawiki_account_config = '/home/eric/.ssh/ebola-robot.json'
data_logfilename = 'ebola-wiki-content-' + today + '.json'
mwaccount = json.load(open(mediawiki_account_config))

mwsite = mwclient.Site(mwaccount['site'], path=mwaccount['sitepath'])
mwsite.login(mwaccount['username'],mwaccount['password'])

for page in mwsite.pages:
    record = {}
    record['title'] = page.page_title
    record['text'] = page.text()
    #print record
    obsess.log_data(record, data_logfilename)
