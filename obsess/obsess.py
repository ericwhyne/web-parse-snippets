#!/usr/bin/python
import nltk.tag.stanford
import re
import mwclient
import sys

def extract_entities(text):
  st = nltk.tag.stanford.NERTagger('lib/english.all.3class.distsim.crf.ser.gz', 'lib/stanford-ner.jar', encoding='utf-8')
  tags = []
  entities = []
  text = re.sub('\n','',text)
  linetags = st.tag(text.split())
  tags.extend(linetags)
  lastcat = ''
  entity = ''
  for linetag in linetags:
    #if linetag[1] != 'O':
      #print "word: " + linetag[0] + " category: " + linetag[1]
    if lastcat == linetag[1]: #if adjacent categories are the same, append together the words
      entity = entity + ' ' + linetag[0]
    else: #this category is different now, start a new entity and write out the old
      if lastcat != 'O':
        if entity:
          entity_record = {u'entity': entity, u'type': lastcat}
          entities.append(entity_record)
          #print entity_record
          #print "Entity: " + entity + " Type: " + lastcat
      entity = linetag[0]
    lastcat = linetag[1]
  return entities


def mediawiki_update(pname, mwuniquething, create, append, mwaccount):
  # pname - the page name
  # mwuniquething - if this string is on the mwpage, the content will not be added (eg: url)
  # create - what to add if the page doesn't already exist
  # append - what to append if the page already exists
  mwsite = mwclient.Site(mwaccount['site'], path=mwaccount['sitepath'])
  mwsite.login(mwaccount['username'],mwaccount['password'])
  page = mwsite.Pages[pname]
  oldpagetxt = page.text()
  newpagetxt = ""
  if page.text() == "":
    print "There is no page for " + pname
    newpagetxt = create + append
  else:
    print "A page exists for " + pname
    newpagetxt = oldpagetxt + append
  print "Checking page for: " + mwuniquething
  #if re.match('.*' + re.escape(mwuniquething) + '.*', page.text()):
  if mwuniquething in oldpagetxt:
    print "This article was already on the page. Ignoring"
  else:
    print "Proposed new page content:\n----------------------------\n" + newpagetxt + "\n-----------------------------------\n"
    if query_yes_no("Edit the page?"):
      print "Editing the page"
      page.save(newpagetxt, summary='automated update')

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
