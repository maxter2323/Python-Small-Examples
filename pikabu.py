import urllib.request
import sys
import chardet
from html.parser import HTMLParser
from datetime import datetime

pikabuUrl = 'http://pikabu.ru/top50_comm.php'
startTag = 'profile_commented'
endTag = 'b-sidebar-sticky'
newsTag = 'a'
classTag = 'class'
headers = []
links = []

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.readData = False
        self.weAreIn = False

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == classTag:
                if attr[1] == startTag:
                    self.weAreIn = True
        if tag == newsTag and self.weAreIn == True:
            links.append( attr[1])
            self.readData = True

    def handle_data(self, data):
        if self.readData:
            headers.append(data)
            self.weAreIn = False
            self.readData = False

def proceed():
    request = urllib.request.urlopen(pikabuUrl)
    content = request.read()

    encoding = chardet.detect(content)['encoding']
    print('Encoding Website: ' + str(encoding))
    print('Encoding Console: ' + str(sys.stdout.encoding))

    html = content.decode(encoding)
    parser = MyHTMLParser()
    parser.feed(html)

def write():
    now = datetime.now();
    separator = '-'
    timestring = str(now.hour) + separator + str(now.minute) + separator + str(now.second) + separator + str(now.day) + separator +str(now.month) + separator + str(now.year)

    filename = str("pikabu " + timestring + '.txt')
    outputFile = open(filename, "a")

    counter = 1
    for header, link in zip(headers, links):
        finalstr = str(str(counter) + '. ' + header + ' : ' + link)
        outputFile.write(finalstr + "\n")
        counter+=1
        print(finalstr)

    outputFile.close()
    print ("Saved to: " + filename)

print ("Pikabu Top 50 Comments")
proceed()
write()
input("Press Enter To Exit")