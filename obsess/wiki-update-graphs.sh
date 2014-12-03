#!/bin/bash
date=`date --iso`
epoch=`date +%s`
wikiaccount="/home/eric/.ssh/ebola-robot.json"
serverip="ebola-wiki.com"
graphdatadir='graph_data/'
contentfile=data/content/ebola-wiki-dev-content-$date.json
graphfile=data/content/ebola-wiki-dev-graphs-$date.zip
rm -f $contentfile
echo downloading content from $wikiaccount to $contentfile
./wiki-download.py $wikiaccount $contentfile
# Generate sub graphs
rm $graphdatadir*
echo generating graph one
./wiki-make-sub-graphs.py $contentfile $graphdatadir 1 minlinks-1
echo generating graph two
./wiki-make-sub-graphs.py $contentfile $graphdatadir 2 minlinks-2
echo generating graph three
./wiki-make-sub-graphs.py $contentfile $graphdatadir 3 minlinks-3
echo generating graph 4
./wiki-make-sub-graphs.py $contentfile $graphdatadir 4 minlinks-4
echo generating graph 5
./wiki-make-sub-graphs.py $contentfile $graphdatadir 5 minlinks-5
echo generating graph 6
./wiki-make-sub-graphs.py $contentfile $graphdatadir 6 minlinks-6
echo generating graph 7
./wiki-make-sub-graphs.py $contentfile $graphdatadir 7 minlinks-7
rm -f $graphfile
zip -r $graphfile $graphdatadir
scp -i ~/.ssh/genericworkkey.pem $graphfile ubuntu@$serverip:~/apps/mediawiki/htdocs/ && ssh -i ~/.ssh/genericworkkey.pem ubuntu@$serverip "rm ~/apps/mediawiki/htdocs/graph_data/*"
ssh -i ~/.ssh/genericworkkey.pem ubuntu@$serverip "unzip -d ~/apps/mediawiki/htdocs/ ~/apps/mediawiki/htdocs/ebola-wiki-dev-graphs-$date.zip"

scp -i ~/.ssh/genericworkkey.pem graphs/graph_make.js ubuntu@$serverip:~/apps/mediawiki/htdocs/
ssh -i ~/.ssh/genericworkkey.pem ubuntu@$serverip "sed -i 's/graph_make.js.*\"/graph_make.js\?$epoch\"/' ~/apps/mediawiki/htdocs/skins/Vector.php"

scp -i ~/.ssh/genericworkkey.pem graphs/graph_style.css ubuntu@$serverip:~/apps/mediawiki/htdocs/
ssh -i ~/.ssh/genericworkkey.pem ubuntu@$serverip "sed -i 's/graph_style.css.*\"/graph_style.css\?$epoch\"/' ~/apps/mediawiki/htdocs/skins/Vector.php"


scp -i ~/.ssh/genericworkkey.pem graphs/d3.v3.min.js ubuntu@$serverip:~/apps/mediawiki/htdocs/

# ensure graph div exists on each page
#./wiki-append-graph.py
