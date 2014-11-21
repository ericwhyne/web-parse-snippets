#!/usr/bin/python
import json
import obsess

#mediawiki_account_config = '/home/eric/.ssh/ebola-robot.json'
filename = 'proposed_changes.json'

logfile = open(filename, 'r')
records = json.load(logfile)
logfile.close()

#proposed_change = {'name':normalized_entity_name,'type':record[u'type'],'unique_attrib':mwuniquething,'create':create,'append':append,'mwaccount':mediawiki_account}
for record in records:
    obsess.mediawiki_update(record['name'], record['type'], record['unique_attrib'], record['create'], record['append'], record['mwaccount'])
