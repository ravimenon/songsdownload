#!/usr/bin/python
from HTMLParser import HTMLParser
import urllib2
import json
import re
import sys

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data=[]

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href" and re.match(r'^http.*\.mp3$',attr[1]):
                    self.data.append(attr[1])

def wget(url):
    url=url.replace(" ","%20");
    req=urllib2.Request(url);
    if url:
        try:
            response = urllib2.urlopen(req,timeout=55);
            html = response.read()
            return html
        except urllib2.HTTPError, e:    
			print str(e.code) + " error"
			return None
    else:
        print "Search didn't fetch any result"

def google_search(page):
    page=str(page);
    print "Googling page " + page;
    gkey='AIzaSyAxoxKFaWHdn3otGrzggUr1Oa2gvhLUOpc';
    gcx='006551824314330792304:xompbxiw3xa';
    search_query='https://www.googleapis.com/customsearch/v1?key=' + gkey + '&cx=' + gcx + '&q=' + movie + '&start=' + page;
    google_result = wget(search_query);
    try:
        return json.loads(google_result)
    except:
        return None;

def extractSongURL(link):
    htmlparser=MyHTMLParser()
    print link;
    wget_link=wget(link);
    if(wget_link != None):
        htmlparser.feed(wget(link))
    	for song_url in htmlparser.data:
        	if link in all_songs:
        	    all_songs[link].append(song_url)
        	else:
        	    all_songs[link]=[song_url]

def download(link):
    song_urls = all_songs.get(link)
    for song_url in song_urls:
        file_name = song_url.split('/')[-1].replace("%20","").replace(" ","");
        print "Downloading " + file_name;
        raw_song = wget(song_url)
        if(raw_song != None):
        	song = open(file_name,'wb')
        	song.write(raw_song)
        	song.close()
    var = raw_input("Enter to continue | (Q)uit : ")
    if var == "Q" or var == "q":
    	sys.exit(0)

def display_and_download(link):
    song_urls = all_songs.get(link)
    print link;
    try:
        for song_url in song_urls:
            print  "\t" + song_url
    except:
            return
    var = raw_input("Download (Y)es | (Q)uit | Enter to continue: ")
    if var == "Y" or var == "y":
        download(link)
    elif var=="Q" or var=="q":
        sys.exit(0)

movie=sys.argv[1]
page=1;
all_songs=dict();

while(page<5):
    google_json_results = google_search(page)           #TODO: break if less than 5 pages
    page=page+1
    try:
        total_site = len(google_json_results['items'])  #Add exception here
    except:
        print "Sorry no more results"
        sys.exit(0)
    print "Found " + str(total_site) + " results"
    for google_result in google_json_results['items']:
            song_site=google_result['link'];
            extractSongURL(song_site)
            display_and_download(song_site)

