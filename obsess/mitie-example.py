#!/usr/bin/python
#
# This example shows how to use the MITIE Python API to perform named entity
# recognition and also how to run a binary relation detector on top of the
# named entity recognition outputs.
#
import sys, os
# Make sure you put the mitielib folder into the python search path.  There are
# a lot of ways to do this, here we do it programmatically with the following
# two statements:
parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent + '/lib/MITIE/mitielib')

print parent

import mitie

print "loading NER model..."
ner = mitie.named_entity_extractor('lib/MITIE/english/ner_model.dat')
print "\nTags output by this NER model:", ner.get_possible_ner_tags()

# Load a text file and convert it into a list of words.
tokens = mitie.tokenize(mitie.load_entire_file('lib/MITIE/sample_text.txt'))
print "Tokenized input:", tokens

entities = ner.extract_entities(tokens)
print "\nEntities found:", entities
print "\nNumber of entities detected:", len(entities)

for e in entities:
    range = e[0]
    tag = e[1]
    entity_text = " ".join(tokens[i] for i in range)
    print "    " + tag + ": " + entity_text
