#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import chardet
import sys
import codecs
from html.parser import HTMLParser

lentaUrl = 'http://lenta.ru/'
starTag = 'b-yellow-box__header bordered-title'
endTag = 'b-sidebar-sticky'
newsTag = 'a'
classTag = 'class'
separator = '---------------------------------------------------------------------------------------'
news = []

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.readData = False
        self.weAreIn = False

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == classTag:
                if attr[1] == starTag:
                    self.weAreIn = True
                if attr[1] == endTag:
                    self.weAreIn = False
        if tag == newsTag and self.weAreIn == True:
            news.append(separator)
            self.readData = True
        else:
            self.readData = False

    def handle_data(self, data):
        if self.readData:
            news.append(data)

def proceed():
    request = urllib.request.urlopen(lentaUrl)
    content = request.read()

    encoding = chardet.detect(content)['encoding']
    print('Encoding of the website: ' + str(encoding))
    print('Encoding of the console: ' + str(sys.stdout.encoding))

    html = content.decode('utf-8', errors='replace')
    parser = MyHTMLParser()
    parser.feed(html)

def show():
    finalOutput = []
    tempword = ' '
    for word in news:
        if word == separator:
           finalOutput.append(tempword)
           finalOutput.append(separator)
           tempword = ' '
        else:
            tempword = tempword + ' '  + word
    for f in finalOutput:
        bytes = str.encode(f)
        toPrint = bytes.decode('utf-8', errors='replace')
        print (toPrint)

print ("LENTA NEWS:")

try:
    proceed()
    show()
except Exception as e:
    print ("Error " + str(e.errno) + ' ' + str(e.strerror))

print ("")
input("Press Enter To Exit")