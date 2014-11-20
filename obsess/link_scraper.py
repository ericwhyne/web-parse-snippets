#!/usr/bin/python
import urllib2
import json
import re
from goose import Goose
import summarize
import obsess
from collections import defaultdict
from bs4 import BeautifulSoup

urls = ["http://online-jihad.com/",
"http://online-jihad.com/",
"http://online-jihad.com/2013/04/27/jihadi-twitter-activism-introduction/",
"http://online-jihad.com/category/jihadica/",
"http://online-jihad.com/category/online-jihad/",
"http://www.jihadica.com/jihadi-twitter-activism-introduction/",
"http://online-jihad.com/2012/09/18/fatwa-calling-for-the-death-of-the-director-producer-and-actors-involved-in-making-the-filminnocence-of-muslims/",
"http://online-jihad.com/2012/01/25/jabha-al-nusra-a-new-jihadi-group-in-syria/",
"http://online-jihad.com/category/jihadist-ideology/",
"http://online-jihad.com/category/online-jihad/",
"http://online-jihad.com/category/syria/",
"http://online-jihad.com/2012/01/25/jabha-al-nusra-a-new-jihadi-group-in-syria/",
"http://online-jihad.com/2011/12/12/aqim-issues-statement-kidnapping-5-eu-citizens/",
"http://online-jihad.com/category/aqim-al-qaeda-in-africa-primarily-algeria-mali-and-mauretania/",
"http://online-jihad.com/category/online-jihad/",
"http://online-jihad.com/2011/12/12/aqim-issues-statement-kidnapping-5-eu-citizens/",
"http://online-jihad.com/2011/04/13/book-announcement-studying-jihadism/",
"http://online-jihad.com/category/blog-news/",
"http://online-jihad.com/category/blogroll/",
"http://online-jihad.com/category/jihadist-ideology/",
"http://online-jihad.com/2011/04/13/book-announcement-studying-jihadism/",
"http://online-jihad.com/2011/01/11/10-methods-to-detect-and-foil-the-plots-of-spies-abou-zakaria/",
"http://online-jihad.com/category/jihadis-using-non-arabic-sources/counter-counter-terrorism/",
"http://online-jihad.com/category/crazy-english-jihad-forum/",
"http://www.majahden.com/from/showthread.php?p=135",
"http://www.majahden.com/from/showthread.php?p=205",
"http://www.majahden.com/from/showthread.php?t=199",
"http://www.nytimes.com/2010/11/28/us/28portland.html?pagewanted=all",
"http://news.bbc.co.uk/2/hi/south_asia/1804228.stm",
"http://online-jihad.com/2010/11/19/%e2%80%9cfursan-al-shahada-part-8%e2%80%9d-highlights-nigeria-and-central-africa/",
"http://online-jihad.com/category/aqim-al-qaeda-in-africa-primarily-algeria-mali-and-mauretania/",
"http://online-jihad.com/category/islamic-state-of-iraq-isi/",
"http://online-jihad.com/2010/11/19/%e2%80%9cfursan-al-shahada-part-8%e2%80%9d-highlights-nigeria-and-central-africa/#comments",
"http://online-jihad.com/page/2/",
"http://online-jihad.com/2013/04/27/jihadi-twitter-activism-introduction/",
"http://online-jihad.com/2012/09/18/fatwa-calling-for-the-death-of-the-director-producer-and-actors-involved-in-making-the-filminnocence-of-muslims/",
"http://online-jihad.com/2012/01/25/jabha-al-nusra-a-new-jihadi-group-in-syria/",
"http://online-jihad.com/category/1980s-jihad-vs-soviets/",
"http://online-jihad.com/category/afpak/",
"http://online-jihad.com/category/ansar-as-sunna-iraq/",
"http://online-jihad.com/category/aq-arab-peninsula-saudi-arabia/",
"http://online-jihad.com/category/aq-arab-peninsula-yemen/",
"http://online-jihad.com/category/aqim-al-qaeda-in-africa-primarily-algeria-mali-and-mauretania/",
"http://online-jihad.com/category/arabic-media/",
"http://online-jihad.com/category/as-sahab-global-jihad-aq-media-outlet/",
"http://online-jihad.com/category/blog-news/",
"http://online-jihad.com/category/blogroll/",
"http://online-jihad.com/category/jihadis-using-non-arabic-sources/counter-counter-terrorism/",
"http://online-jihad.com/category/crazy-english-jihad-forum/",
"http://online-jihad.com/category/global-islamic-media-front-gimf/",
"http://online-jihad.com/category/iraqi-islamic-resistance-front-jaami/",
"http://online-jihad.com/category/islamic-army-in-iraq-iai/",
"http://online-jihad.com/category/islamic-movement-of-uzbekistan-imu/",
"http://online-jihad.com/category/islamic-state-of-iraq-isi/",
"http://online-jihad.com/category/jaysh-al-mujahidin-iraq/",
"http://online-jihad.com/category/jihadica/",
"http://online-jihad.com/category/jihadis-using-non-arabic-sources/",
"http://online-jihad.com/category/jihadist-ideology/",
"http://online-jihad.com/category/misc/",
"http://online-jihad.com/category/online-jihad/",
"http://online-jihad.com/category/palestine/",
"http://online-jihad.com/category/sawt-al-jihad/",
"http://online-jihad.com/category/syria/",
"http://online-jihad.com/category/uncategorized/",
"http://onlinejihad.wordpress.com",
"http://online-jihad.com/2013/04/",
"http://online-jihad.com/2012/09/",
"http://online-jihad.com/2012/01/",
"http://online-jihad.com/2011/12/",
"http://online-jihad.com/2011/04/",
"http://online-jihad.com/2011/01/",
"http://online-jihad.com/2010/11/",
"http://online-jihad.com/2010/09/",
"http://online-jihad.com/2010/05/",
"http://online-jihad.com/2010/04/",
"http://online-jihad.com/2010/03/",
"http://online-jihad.com/2010/02/",
"http://online-jihad.com/2010/01/",
"http://online-jihad.com/2009/12/",
"http://online-jihad.com/2009/11/",
"http://online-jihad.com/2009/05/",
"http://online-jihad.com/2009/04/",
"http://online-jihad.com/2009/02/",
"http://online-jihad.com/2009/01/",
"http://online-jihad.com/2008/12/",
"http://online-jihad.com/2008/10/",
"http://online-jihad.com/2008/09/",
"http://online-jihad.com/2008/06/",
"http://online-jihad.com/2008/05/",
"http://online-jihad.com/2008/03/",
"http://online-jihad.com/2007/12/",
"http://online-jihad.com/2007/11/",
"http://online-jihad.com/2007/10/",
"http://online-jihad.com/2007/09/",
"http://online-jihad.com/2007/07/",
"http://online-jihad.com/2007/06/",
"http://online-jihad.com/2007/05/",
"http://online-jihad.com/2007/04/",
"http://online-jihad.com/2007/03/",
"http://online-jihad.com/2007/02/",
"http://online-jihad.com/2009/12/21/more-hamas-bashing-from-jihadist-forums/",
"http://online-jihad.com/2007/02/15/algeria-tanzim-al-qa%e2%80%99ida-fi-bilad-al-maghreb-al-islam-airs-new-video/",
"http://online-jihad.com/2010/02/28/as-sahab-videotranscript-of-abu-dujana-al-khurasani/",
"http://online-jihad.com/2010/11/18/new-%e2%80%9cfursan-al-shahada%e2%80%9d-video-about-nigeria/",
"http://online-jihad.com/2013/04/27/jihadi-twitter-activism-introduction/",
"http://online-jihad.com/2010/02/22/jihadis-claim-executed-murderer-a-mujahid/",
"http://online-jihad.com/2010/04/15/al-falluja-forum-announces-new-styles-al-ekhlaas-and-al-hisbah/",
"http://online-jihad.com/2010/02/22/taliban-issue-new-edition-of-magazine-al-somood-no-45/",
"http://online-jihad.com/2007/09/14/update-al-mafqud-%e2%80%93-missing-in-action/",
"http://online-jihad.com/2010/02/27/abu-dujana-al-khorasani-%e2%80%93-new-propaganda-material/",
"https://onlinejihad.wordpress.com/wp-login.php",
"http://online-jihad.com/feed/",
"http://online-jihad.com/comments/feed/"]

mediawiki_account_config = '/home/eric/.ssh/jihadi-robot.json'
data_logfilename = 'jihad_scrape.json'

mediawiki_account = json.load(open(mediawiki_account_config))
ss = summarize.SimpleSummarizer()

headers = { 'User-Agent' : 'Magic Browser' }
for url in urls:
  if obsess.url_not_in_log_file(url, data_logfilename):
    data = {}
    data['url'] = url
    all_entities = []
    print "\n\n*****************\n"
    print "Fetching web page: " + url
    req = urllib2.Request(url, None, headers)
    raw_html = urllib2.urlopen(req).read()
    data['raw_html'] = raw_html
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

    #print "Tagging - Stanford NER..."
    #stanford_title_entities = obsess.stanford_extract_entities(title)
    #stanford_article_entities = obsess.stanford_extract_entities(article.cleaned_text)
    #all_entities +=  stanford_title_entities + stanford_article_entities
    #print stanford_title_entities
    #print stanford_article_entities
    #data['stanford_title_entities'] = stanford_title_entities
    #data['stanford_article_entities'] = stanford_article_entities

    print "Tagging article - MITIE..."
    mitie_title_entities = obsess.mitie_extract_entities(title)
    mitie_article_entities = obsess.mitie_extract_entities(article.cleaned_text)
    all_entities += mitie_title_entities + mitie_article_entities
    print mitie_title_entities
    print mitie_article_entities

    print "Tagging article - known..."
    known_title_entities = obsess.known_extract_entities(title)
    known_article_entities = obsess.known_extract_entities(article.cleaned_text)
    all_entities += known_title_entities + known_article_entities
    print known_title_entities
    print known_article_entities

    print "Logging captured data..."
    obsess.log_data(data, data_logfilename)

    all_unique_entities = [dict(t) for t in set([tuple(record.items()) for record in all_entities])]

    for record in all_unique_entities:
      print "Generating article summary for entity " + record[u'entity'] + " - " + record[u'type']
      article_summary = ss.summarize(article.cleaned_text, 4, record[u'entity'])
      print "Summary: " + article_summary + "\n\n"
      normalized_entity_name = re.sub('\.','',record[u'entity']) #remove periods from acronyms and names to be consistent
      mwuniquething = url # if this thing already exists on the mwpage, the content will not be appended
      if article_summary:
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
      else:
        print "No summary available, skipping."
