import requests, time, datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS

def getHTML(billWurtzURL: str) -> bytes:
    clientConnection = urlopen(billWurtzURL)
    billWurtzHTML = clientConnection.read()
    clientConnection.close()
    return billWurtzHTML

def makeSoup(billWurtzHTML: bytes) -> BS:
    pageSoup = BS(billWurtzHTML, 'html.parser')
    return pageSoup

def getVideoFiles(pageSoup: BS) -> [('videoName','videoFile')]:
    videoList = [(video.get_text(),video['href']) for video in pageSoup.find_all('a', href=True)]
    videoListLength = len(videoList)
    return videoList, videoListLength

def downloadVideos(videoList: [('videoName','videoFile')], billWurtzURL: str, askedDirectory: str, videoListLength: int) -> None:
    for videoFile in videoList:
        video = requests.get(billWurtzURL+videoFile[1], stream = True)
        videoName = videoFile[0].replace(':', '.')
        open(f'{askedDirectory}\\#{videoListLength} {videoName}.mp4','wb').write(video.content)
        videoListLength -= 1
        print(f'Downloaded {billWurtzURL+videoFile[1]} to {askedDirectory} ')

def main():
    billWurtzURL = 'https://billwurtz.com/reality/'
    billWurtzHTML = getHTML(billWurtzURL)
    pageSoup = makeSoup(billWurtzHTML)
    videoList, videoListLength = getVideoFiles(pageSoup)
    askedDirectory = input("Where would you like to put these videos? (Directory): ")
    print('Starting...')
    startingTime = time.clock()
    downloadVideos(videoList, billWurtzURL, askedDirectory, videoListLength)
    endingTime = time.clock()
    hours,minutes,seconds = str(datetime.timedelta(seconds = endingTime - startingTime)).split(':')
    
    print(f'Finished! Process took {hours} hours {minutes} minutes and {seconds} seconds')
    
if __name__ == '__main__':
    main()

    