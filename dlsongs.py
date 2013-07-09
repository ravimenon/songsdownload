#!/usr/bin/python
from HTMLParser import HTMLParser
import urllib2
import json
import re
import sys

def rawSongDownload(songs_url):
    for song_url in songs_url:
        file_name = song_url.split('/')[-1].replace("%20","").replace(" ","");
        print "Downloading " + file_name;
        raw_song = wget(song_url)
        if(raw_song != None):
            song = open(file_name,'wb')
            song.write(raw_song)
            song.close()

def wget(url):
    url = url.replace(" ","%20")
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req,timeout=55);
        html = response.read()
        return html
    except urllib2.HTTPError, e:
        print str(e.code) + " error"
        return None


class HTMLToSong(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data=[]

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href" and re.match(r'^http.*\.mp3$',attr[1]):
                    self.data.append(attr[1])


class Google():
    def __init__(self):
        gkey = 'AIzaSyAxoxKFaWHdn3otGrzggUr1Oa2gvhLUOpc'
        gcx = '006551824314330792304:xompbxiw3xa'
        self.queryurl = 'https://www.googleapis.com/customsearch/v1?key=' + gkey + '&cx=' + gcx #+ '&q=' + movie + '&start=' + page;


    def search(self, query, page):
        google_json_results = {}
        self.queryurl = self.queryurl + '&q=' + query + '&start=' + str(page);
        google_raw_result = wget(self.queryurl)
        try:
            google_json_results = json.loads(google_raw_result)
        except:
            print "ERROR: Google search failed"
                                                                                # TODO: Exit here
        for google_result in google_json_results['items']:
            yield google_result['link']

class Song():
    def __init__(self):
        pass

    def download(self,songlinkurls):
        for songlinkurl in iter(songlinkurls):
            htmlparser = HTMLToSong()
            print songlinkurl
            htmlparser.feed(wget(songlinkurl))
            for song in htmlparser.data:
                print "\t",song
            var = raw_input("Download (Y)es | (Q)uit | Enter to continue: ")
            if var == "Y" or var == "y":
                rawSongDownload(songs)
            elif var=="Q" or var=="q":
                sys.exit(0)

def main():
    # Settings
    query = "chennai express"
    page = 1
    resultpages_count = 10
    google = Google()
    songs = Song()
    google_results = google.search(query,page)
    songs.download(google_results)


if __name__ == "__main__":
    main()
