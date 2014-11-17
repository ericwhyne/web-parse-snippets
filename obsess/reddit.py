#!/usr/bin/python
import urllib2
import json
import re
from goose import Goose
import summarize
import obsess

subreddit_url = "http://api.reddit.com/r/ebola"
#subreddit_url = "http://api.reddit.com/r/ebola/new/"
#subreddit_url = "http://api.reddit.com/r/EbolaNewsBot/"

mediawiki_account_config = '/home/eric/.ssh/ebola-robot.json'

mediawiki_account = json.load(open(mediawiki_account_config))


headers = { 'User-Agent' : 'ObsessBot/alphadev' } # reddit heavily throttles default user agents
req = urllib2.Request(subreddit_url, None, headers)
text = urllib2.urlopen(req).read()

#text = urllib.urlopen(subreddit_url).read()
records = json.loads(text)

if re.match('^{\"error.*', text):
  print "Error: " + text
else:
  #for key in records.keys():
  for listing in records[u'data'][u'children']:
    title = listing[u'data'][u'title']
    url = listing[u'data'][u'url']
    domain = listing[u'data'][u'domain']
    permalink = 'http://reddit.com' + listing[u'data'][u'permalink']
    print "\n\n*****************\n" + title
    print "Tagging title..."
    title_entities = obsess.extract_entities(title)
    print title_entities
    g = Goose()
    article = g.extract(url=url)
    print "Tagging article..."
    article_entities = obsess.extract_entities(article.cleaned_text)
    ss = summarize.SimpleSummarizer()
    all_entities = title_entities + article_entities #TODO: this will still have duplicates. It's only ineffecient but deduped below.
    print "All entities: " + str(all_entities)
    for record in all_entities:
      print "Generating article summary for entity " + record[u'entity'] + " - " + record[u'type']
      article_summary = ss.summarize(article.cleaned_text, 4, record[u'entity'])
      print "Summary: " + article_summary + "\n\n"
      normalized_entity_name = re.sub('\.','',record[u'entity']) #remove periods from acronyms and names to be consistent
      mwuniquething = url # if this thing already exists on the mwpage, the content will not be appended
      if record[u'type'] == 'LOCATION':
        gmaps_url = 'http://maps.google.com/?q=' + re.sub(' ','+', record[u'entity'])
        create = "[[category:locations]]\nView in google maps: " + gmaps_url + "\n"
        append = "\n\n\n" + title + "\n* " + url + "\n* Summary: " + article_summary + "\n* Source: [[" + domain + "]] \n" + "* [" + permalink + " Discus on Reddit]\n\n"
        obsess.mediawiki_update(normalized_entity_name, record[u'type'], mwuniquething, create, append, mediawiki_account)
      elif record[u'type'] == 'PERSON':
        create = "[[category:people]]\n"
        append = "\n\n\n" + title + "\n* " + url + "\n* Summary: " + article_summary + "\n* Source: [[" + domain + "]]\n" + "* [" + permalink + " Discus on Reddit]\n\n"
        obsess.mediawiki_update(normalized_entity_name, record[u'type'], mwuniquething, create, append, mediawiki_account)
      elif record[u'type'] == 'ORGANIZATION':
        create = "[[category:organizations]]\n"
        append = "\n\n\n" + title + "\n* " + url + "\n* Summary: " + article_summary + "\n* Source: [[" + domain + "]] \n" + "* [" + permalink + " Discus on Reddit]\n\n"
        obsess.mediawiki_update(normalized_entity_name, record[u'type'], mwuniquething, create, append, mediawiki_account)




#TODO: pseudocode for mediawiki content integration
# Check to make sure Entity is sane and not an ignored entity TODO: create ignored entity file
# If it is, attempt to create a wiki page with Entity as the wiki page name, category as entity type.
