#!/usr/bin/python
import json
import obsess

#mediawiki_account_config = '/home/eric/.ssh/ebola-robot.json'
filename = 'proposed_changes.json'
rejectsfilename = 'mediawiki_update_rejects.json'
logfile = open(filename, 'r')
records = json.load(logfile)
logfile.close()

#proposed_change = {'name':normalized_entity_name,'type':record[u'type'],'unique_attrib':mwuniquething,'create':create,'append':append,'mwaccount':mediawiki_account}
for record in records:
    rejects = json.load(open(rejectsfilename, 'r'))
    rejectflag = False
    for reject in rejects:
      if record['name'] == reject['entity'] and record['type'] == reject['type']:
          rejectflag = True
          print "Rejected: " + record['name'] + " as " + record['type']
    if rejectflag == False:
      print "Updating.."
      obsess.mediawiki_update(record['name'], record['type'], record['unique_attrib'], record['create'], record['append'], record['mwaccount'], rejectsfilename)
