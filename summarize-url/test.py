#!/usr/bin/python
import summarize
import urllib
from bs4 import BeautifulSoup
import re

html = urllib.urlopen('http://www.bbc.com/news/world-latin-america-29984688').read()
soup = BeautifulSoup(html)

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

relevant = ""
for chunk in chunks:
  if chunk:
    chunk = re.sub('\s+',' ', chunk) #reduct all adjacent whitespace characters to just one space character
    if len(chunk.split(' ')) > 5:
      relevant += chunk + ' \n'

ss = summarize.SimpleSummarizer()
input = "NLTK is a python library for working human-written text. Summarize is a package that uses NLTK to create summaries."
print ss.summarize(relevant.encode('utf-8'), 4)
