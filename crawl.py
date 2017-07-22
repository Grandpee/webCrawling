from bs4 import BeautifulSoup
import re
import urllib2
import time
import json
import os

URL = "https://www.youtube.com/watch?v="

videoID = []
#videoName = []
viewCount = []
notAvailable = []
_timeList = []
localTimeList = []
i = 0
noVideo = 0


with open (os.path.join(os.getcwd(), 'vids1k.txt'), "r") as inFile:
    for line in inFile.readlines():
        line = line.replace('\n', '')
        videoID.append(line) 

inFile.close()


def videoInfo(URL, videoid):
    URL = URL + videoid
    request = urllib2.Request(URL)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response, "html5lib")

    _time = time.time()
    localTime = time.asctime(time.localtime(_time))

    _timeList.append(_time)
    localTimeList.append(localTime)
   
    try:
        #videoTitle = soup.find("span", {"class":"watch-title"}).get_text()
        #videoTitle = videoTitle.replace('\n', '').replace('\t', '')
        #videoName.append(videoTitle)

        views = soup.find("div", {"class":"watch-view-count"}).get_text()
        c = re.findall("[0-9]+", views)
        count = ''
        for a in c:
            count = count + str(a)

        viewCount.append(count)
    except Exception as ex:
        print (ex)
        global noVideo
        noVideo += 1
        notAvailable.append(videoid)

_round = 0
while (True):

    startTime = time.time()
    count = 0
    for _id in videoID:
        #print (count)
        count += 1
        videoInfo(URL, _id)
        time.sleep(0.2)


    localTime = time.asctime(time.localtime(time.time()))
    filePath = os.path.join(os.getcwd(), 'outData')
    fileName = "out_" + str(_round)

    with open(os.path.join(filePath, fileName), "w") as outFile:
        for iteration in range(len(videoID)-noVideo):
            writeOut = {
                    "videoID" : videoID[iteration],
                    #"videoName" : videoName[iteration],
                    "viewCount" : viewCount[iteration],
                    "localTime" : localTimeList[iteration],
                    "_time" : _timeList[iteration]}
            json.dump(writeOut, outFile)
            outFile.write("\n")

    outFile.close()

    endTime = time.time()

    _round += 1

    processTime = endTime - startTime
    
    print ("the overall time is: " + str(processTime))
    print ("there are " + str(noVideo) + " videos no longer available!")

    time.sleep(1200 - (processTime))

    viewCount = []
    _timeList = []
    localTimeList = []

    if (len(notAvailable) > 0):
        for iden in notAvailable:
            videoID.remove(iden)

        notAvailable = []

    
