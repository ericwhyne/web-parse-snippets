#!/usr/bin/python
import urllib2
import json
import re
from goose import Goose
import summarize
import obsess
from collections import defaultdict
from bs4 import BeautifulSoup
#########################################################################################################################
# Configuration
subreddit_url = "http://api.reddit.com/r/ebola"
#subreddit_url = "http://api.reddit.com/r/EbolaNewsBot/"
#subreddit_url = "http://api.reddit.com/r/EbolaGooglers"
#subreddit_url = "http://api.reddit.com/r/ebolasurvival"
#subreddit_url = "http://api.reddit.com/r/ebolawestafrica"
#subreddit_url = "http://api.reddit.com/r/ebolaUS

mediawiki_account_config = '/home/eric/.ssh/ebola-robot.json'
data_logfilename = 'ebola_scrape.json'
proposed_change_filename = 'ebola_wiki_proposed_changes.json'
#########################################################################################################################
# initialization
mediawiki_account = json.load(open(mediawiki_account_config))
ss = summarize.SimpleSummarizer()

# Fetch the post from the Reddit sub
headers = { 'User-Agent' : 'ObsessBot/alphadev' } # reddit heavily throttles default user agents
req = urllib2.Request(subreddit_url, None, headers)
text = urllib2.urlopen(req).read()
reddit_posts = json.loads(text)

# See if it failed
if re.match('^{\"error.*', text):
  print "Error: " + text
else:
  for reddit_post in reddit_posts[u'data'][u'children']:
   data = {} # this is the object which will collect all data and be logged for export
   data['url'] = reddit_post[u'data'][u'url']
    if obsess.url_in_log_file(data['url'], data_logfilename):
      print "Already processed url, skipping. " + data['url']
      continue
    print "\n\n*****************\n"
    if fetched_data = fetch_data(url): # data['raw_html'] data['content_type'] data['page_links'] data['title'] data['cleaned_text']
      data.update(fetched_data)
    else:
      print "Fetching failed, skipping this url."
      continue
#########################################################################################################################
# entity extraction
    all_entities = []
    print "Tagging - Stanford NER..."
    try:
      stanford_title_entities = data['stanfordner_title_entities'] = obsess.stanford_extract_entities(data['title'])
      stanford_article_entities = data['stanfordner_article_entities'] = obsess.stanford_extract_entities(data['cleaned_text'])
      all_entities +=  stanford_title_entities + stanford_article_entities
    except:
      print "Stanford NER failed."
    print "Tagging article - MITIE..."
    try:
      mitie_title_entities = data['mitie_title_entities'] = obsess.mitie_extract_entities(data['title'])
      mitie_article_entities = data['mitie_article_entities'] = obsess.mitie_extract_entities(data['cleaned_text'])
      all_entities += mitie_title_entities + mitie_article_entities
    except:
      print "MITIE failed."
    print "Tagging article - known..."
    try:
      known_title_entities = data['known_title_entities'] = obsess.known_extract_entities(data['title'])
      known_article_entities = data['known_article_entities'] =  obsess.known_extract_entities(data['cleaned_text'])
      all_entities += known_title_entities + known_article_entities
    except:
      print "Failed tagging known."
    all_unique_entities = [dict(t) for t in set([tuple(record.items()) for record in all_entities])]
############################################################################################################################
# logging
    print "Logging captured data..."
    obsess.log_data(data, data_logfilename)
############################################################################################################################
# generating wiki content
    for record in all_entities:
      print "Generating article summary for entity " + record[u'entity'] + " - " + record[u'type']
      article_summary = ss.summarize(article.cleaned_text, 4, record[u'entity'])
      print "Summary: " + article_summary + "\n\n"

      normalized_entity_name = re.sub('\.','',record[u'entity']) #remove periods from acronyms and names to be more consistent in the wiki
      mwuniquething = url # if this thing already exists on the mwpage, the content will not be appended
      reddit_title = reddit_post[u'data'][u'title']
      reddit_domain = reddit_post[u'data'][u'domain']
      reddit_permalink = 'http://reddit.com' + reddit_post[u'data'][u'permalink']
      create = ''
      append = ''
      valid = False
      if record[u'type'] == 'LOCATION':
        gmaps_url = 'http://maps.google.com/?q=' + re.sub(' ','+', record[u'entity'])
        create = "[[category:locations]]\nView in google maps: " + gmaps_url + "\n"
        valid = True
      elif record[u'type'] == 'PERSON':
        create = "[[category:people]]\n"
        valid = True
      elif record[u'type'] == 'ORGANIZATION':
        create = "[[category:organizations]]\n"
        valid = True
      append = "\n\n\n" + reddit_title + "\n* " + url + "\n* Summary: " + article_summary + "\n* Source: [[" + reddit_domain + "]] \n" + "* [" + reddit_permalink + " Discus on Reddit]\n\n"
      if valid == True:
        proposed_change = {'name':normalized_entity_name,'type':record[u'type'],'unique_attrib':mwuniquething,'create':create,'append':append,'mwaccount':mediawiki_account}
        obsess.log_data(proposed_change, proposed_change_filename)
