#!/usr/bin/python
import urllib
from bs4 import BeautifulSoup
import re
import sys

url = "http://www.who.int/csr/disease/ebola/situation-reports/en/"
print url
print "\n\n"

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

#debug line for looking a what we are getting:
print soup.prettify().encode('utf-8')

#TODO: numbers are available as CSV on the WHO page. 
