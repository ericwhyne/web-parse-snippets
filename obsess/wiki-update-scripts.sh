#!/bin/bash
date=`date --iso`
epoch=`date +%s`

serverip="ebola-wiki.com"
#serverip="54.174.48.45"

scp -i ~/.ssh/genericworkkey.pem graphs/graph_make.js ubuntu@$serverip:~/apps/mediawiki/htdocs/
ssh -i ~/.ssh/genericworkkey.pem ubuntu@$serverip "sed -i 's/graph_make.js.*\"/graph_make.js\?$epoch\"/' ~/apps/mediawiki/htdocs/skins/Vector.php"

scp -i ~/.ssh/genericworkkey.pem graphs/graph_style.css ubuntu@$serverip:~/apps/mediawiki/htdocs/
ssh -i ~/.ssh/genericworkkey.pem ubuntu@$serverip "sed -i 's/graph_style.css.*\"/graph_style.css\?$epoch\"/' ~/apps/mediawiki/htdocs/skins/Vector.php"

#scp -i ~/.ssh/genericworkkey.pem graphs/graph_legend.png ubuntu@$serverip:~/apps/mediawiki/htdocs/

scp -i ~/.ssh/genericworkkey.pem graphs/d3.v3.min.js ubuntu@$serverip:~/apps/mediawiki/htdocs/

# ensure graph div exists on each page
#./wiki-append-graph.py
