#!/usr/bin/python
import urllib2
import json
import re
from goose import Goose
import summarize
import obsess
from collections import defaultdict
from bs4 import BeautifulSoup

urls = ["http://online-jihad.com/"]
mediawiki_account_config = '/home/eric/.ssh/jihadi-robot.json'
data_logfilename = 'jihad_scrape.json'

mediawiki_account = json.load(open(mediawiki_account_config))
ss = summarize.SimpleSummarizer()

headers = { 'User-Agent' : 'Internet Explorer' }

if 1:
  for url in urls:
    data = {}
    data['url'] = url
    print "\n\n*****************\n"
    print "Fetching web page..."
    req = urllib2.Request(url, None, headers)
    raw_html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(raw_html)

    print "Extracting links..."
    page_links = []
    for link in soup.find_all('a'):
      page_links.append(link.get('href'))
    data['page_links'] = page_links

    print "Extracting main text..."
    g = Goose()
    article = g.extract(raw_html=raw_html)
    title = article.title
    data['title'] = title
    data['cleaned_text'] = article.cleaned_text

    print "Tagging - Stanford NER..."
    stanford_title_entities = obsess.stanford_extract_entities(title)
    stanford_article_entities = obsess.stanford_extract_entities(article.cleaned_text)
    print stanford_title_entities
    print stanford_article_entities

    data['stanford_title_entities'] = stanford_title_entities
    data['stanford_article_entities'] = stanford_article_entities

    #print "Tagging article - MITIE..."
    #TODO: scrub text to ascii in the obsess.mitie_ex.. function
    #mitie_title_entities = obsess.mitie_extract_entities(title)
    #mitie_article_entities = obsess.mitie_extract_entities(article.cleaned_text)
    #print mitie_title_entities
    #print mitie_article_entities

    print "Tagging article - known..."
    known_title_entities = obsess.known_extract_entities(title)
    known_article_entities = obsess.known_extract_entities(article.cleaned_text)
    print known_title_entities
    print known_article_entities

    print "Logging captured data..."
    obsess.log_data(data, data_logfilename)

    #TODO: this will still have duplicates. It's only ineffecient but deduped below.
    all_entities = known_title_entities + known_article_entities + stanford_title_entities + stanford_article_entities # + mitie_title_entities + mitie_article_entities
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
        append = "\n\n\n" + title + "\n* " + url + "\n* Summary: " + article_summary + "\n\n"
        obsess.mediawiki_update(normalized_entity_name, record[u'type'], mwuniquething, create, append, mediawiki_account)
      elif record[u'type'] == 'PERSON':
        create = "[[category:people]]\n"
        append = "\n\n\n" + title + "\n* " + url + "\n* Summary: " + article_summary + "\n\n"
        obsess.mediawiki_update(normalized_entity_name, record[u'type'], mwuniquething, create, append, mediawiki_account)
      elif record[u'type'] == 'ORGANIZATION':
        create = "[[category:organizations]]\n"
        append = "\n\n\n" + title + "\n* " + url + "\n* Summary: " + article_summary + "\n\n"
        obsess.mediawiki_update(normalized_entity_name, record[u'type'], mwuniquething, create, append, mediawiki_account)