#!/usr/bin/python
import nltk.tag.stanford
import re
import mwclient
import sys
import json

# Next 4 lines are for MITIE
import os
parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent + '/lib/MITIE/mitielib')
import mitie

# Configurations
known_entities_file = "known_entities.json"
stanford_known_bad_entities_file = "stanford_known_bad_entities.json"
mitie_known_bad_entities_file = "mitie_known_bad_entities.json"

# Load models
st = nltk.tag.stanford.NERTagger('lib/english.all.3class.distsim.crf.ser.gz', 'lib/stanford-ner.jar', encoding='utf-8')
mt = mitie.named_entity_extractor('lib/MITIE/english/ner_model.dat')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

type_to_category = {"LOCATION":"[[category:locations]]","PERSON":"[[category:people]]","ORGANIZATION":"[[category:organizations]]"}

def known_entities():
  ke = json.load(open(known_entities_file))
  return ke
def stanford_known_bad_entities():
  kbe = json.load(open(stanford_known_bad_entities_file))
  return kbe
def mitie_known_bad_entities():
  kbe = json.load(open(mitie_known_bad_entities_file))
  return kbe

def log_data(record, filename):
  if os.path.exists(filename):
    logfile = open(filename, 'r')
    records = json.load(logfile)
    logfile.close()
    records.append(record)
    print records
    logfile = open(filename, 'w')
    json.dump(records, logfile)
    logfile.close()
  else:
    records = [record]
    logfile = open(filename, 'w')
    json.dump(records, logfile)
    logfile.close()

def mitie_extract_entities(text):
  entities = []
  tokens = mitie.tokenize(text)
  mitie_entities = mt.extract_entities(tokens)
  for e in mitie_entities:
      range = e[0]
      tag = e[1]
      entity_text = " ".join(tokens[i] for i in range)
      entity_record = {u'entity': entity_text, u'type': tag}
      if entity_record not in mitie_known_bad_entities():
        entities.append(entity_record)
  return entities

def stanford_extract_entities(text):
  #TODO: make sure st loads fine as a global
  tags = []
  entities = []
  lines = text.split('\n')
  for line in lines:
    linetags = st.tag(line.split())
    tags.extend(linetags)
    lastcat = ''
    entity = ''
    for linetag in linetags:
      if lastcat == linetag[1]: #if adjacent categories are the same, append together the words
        entity = entity + ' ' + linetag[0]
      else: #this category is different now, start a new entity and write out the old
        if lastcat != 'O':
          if entity:
            entity_record = {u'entity': entity, u'type': lastcat}
            if entity_record not in stanford_known_bad_entities():
              entities.append(entity_record)
        entity = linetag[0]
      lastcat = linetag[1]
  return entities

def known_extract_entities(text):
  #TODO: convert text to ascii
  entities = []
  for entity in known_entities(): # bag the entities that the model stinks at finding
    if entity['entity'] in text:
      entities.append(entity)
  return entities

def mediawiki_update(pname, etype, mwuniquething, create, append, mwaccount):
  # pname - the page name
  # mwuniquething - if this string is on the mwpage, the content will not be added (eg: url)
  # create - what to add if the page doesn't already exist
  # append - what to append if the page already exists
  mwsite = mwclient.Site(mwaccount['site'], path=mwaccount['sitepath'])
  mwsite.login(mwaccount['username'],mwaccount['password'])
  page = mwsite.Pages[pname]
  oldpagetxt = page.text()
  newpagetxt = ""
  ask_before_edit = "true"
  if page.text() == "":
    #print "++++ There is no page for " + pname
    newpagetxt = create + "\n\n==Recent News==\n\n" + append
  else:
    if '==Recent News==' in oldpagetxt: # A page exists for " + pname
      newpagetxt = re.sub(re.escape('==Recent News=='),'==Recent News==' + append,oldpagetxt)
      if type_to_category[etype] in oldpagetxt:
        ask_before_edit = "false" # Just make the update if the page of correct type cateogry already exists
    else:
      newpagetxt = oldpagetxt + "\n\n==Recent News==\n\n" + append
  #print "Checking page for: " + mwuniquething
  #if re.match('.*' + re.escape(mwuniquething) + '.*', page.text()):
  if mwuniquething in oldpagetxt:
    print "This article was already on the page. Ignoring\n\n"
  else:
    print "Proposed update: \n" + append + "\n\n"
    if ask_before_edit == "false":
      print bcolors.WARNING + "Unsupervised edit! " + pname + " as " + etype + bcolors.ENDC
      page.save(newpagetxt, summary='automated update')
    else:
      print "\n\nis " + pname + " a " + etype + "?"
      if query_yes_no(bcolors.OKBLUE + "Edit the page?" + bcolors.ENDC):
        print "Editing the page"
        page.save(newpagetxt, summary='automated update')

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer."""
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
