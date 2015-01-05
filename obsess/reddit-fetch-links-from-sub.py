#!/usr/bin/python
import urllib2
import json
import re
import summarize
import obsess
from collections import defaultdict

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
    fetched_data = obsess.fetch_data(data['url'], headers)
    if fetched_data: # data['raw_html'] data['content_type'] data['page_links'] data['title'] data['cleaned_text']
      data.update(fetched_data)
    else:
      print "Fetching failed, skipping this url."
      continue
    print "Logging captured data..."
    obsess.log_data(data, data_logfilename)
