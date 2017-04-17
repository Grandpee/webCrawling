from bs4 import BeautifulSoup

import urllib2   
import re
import time
import json

quoteList = []
URL = "http://quotes.toscrape.com"

#Request URL to crawl data
def url_request(URL):
    time.sleep(1)
    request = urllib2.Request(URL)
    response = urllib2.urlopen(request)
    bsObj = BeautifulSoup(response)
    return bsObj

#Get Content in that Page
def url_getContent(bsObj):
    quotes = bsObj.findAll("div", {"class":"quote"})
    for quote in quotes:
        author = quote.find("small", {"class":"author"}).get_text()
        text = quote.find("span", {"class":"text"}).get_text()
        tags = quote.findAll("a", {"class":"tag"})
        quoteList.append({
            "Author" : author,
            "Quote" : text,
            "Tags" : append_tag(tags),
            })

#For Tag list
def append_tag(tags):
    taglist = []
    for tag in tags:
        taglist.append(tag.get_text())
    return taglist   

#Get next page url-link
def url_getLinks(bsObj):
    try:
        link = bsObj.find("li", {"class":"next"}).find("a", href=re.compile("^(/page/)")).attrs["href"]
        return link
    except AttributeError:
        pass

rep = url_request(URL)

while rep is not None:
    url_getContent(rep)
    linker = url_getLinks(rep)

    if linker is not None:
        print URL+linker
        rep = url_request(URL+linker)
    else:
        rep = None

length_quoteList = len(quoteList)

#write to file with JSON
with open('data.txt', 'w') as outfile:
    for quote in quoteList:
        json.dump(quote, outfile)
        outfile.write('\n')


#for index in range(0, length_quoteList):
#    print quoteList[index]

