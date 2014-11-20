#!/usr/bin/python
import mwclient
import json

mediawiki_account_config = '/home/eric/.ssh/ebola-robot.json'
mwaccount = json.load(open(mediawiki_account_config))

mwsite = mwclient.Site(mwaccount['site'], path=mwaccount['sitepath'])
mwsite.login(mwaccount['username'],mwaccount['password'])

locations = []
for page in mwsite.Categories['locations']:
    locations.append(page.page_title)

people = []
for page in mwsite.Categories['people']:
    people.append(page.page_title)

organizations = []
for page in mwsite.Categories['organizations']:
    organizations.append(page.page_title)

for page in mwsite.pages:
    text = page.text()
    #TODO: now do something!
