import webbrowser
from pocket import Pocket
from HTMLParser import HTMLParser

#Pocket Data
consumer_key = 'YOUR CONSUMER KEY'
redirect_uri = 'https://google.com'

#Parser Data
filename = 'bookmarks.html'
urlList = []
currentTag = 'Python'
headerTag = 'h3'
linkTag = 'href'

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.readData = False

    def handle_starttag(self, tag, attrs):
        if tag == headerTag:
            print tag, self.readData
            self.readData = True

        for attr in attrs:
            if attr[0] == linkTag:
               link = attr[1]
               print "link: ", link
               newPair = [link, currentTag]
               urlList.append(newPair)

    def handle_data(self, data):
        if self.readData:
           print "Tag: ", data
           currentTag = data
           self.readData = False


request_token = Pocket.get_request_token(consumer_key, redirect_uri)
auth_url = Pocket.get_auth_url(request_token,redirect_uri)

webbrowser.open_new_tab(auth_url)
print 'Please authorize the app using the following url and press ENTER here', auth_url
raw_input()

access_token = Pocket.get_access_token(consumer_key=consumer_key, code=request_token)

print 'Got request token', request_token
print 'Got access token', access_token

def add_url(url, tag):
    print 'adding', url
    pocket_instance = Pocket(consumer_key, access_token)
    print pocket_instance.add(url=url, tags=[tag])


file = open(filename, 'r')
content = file.read()
file.close()

parser = MyHTMLParser()
parser.feed(content)

print 'Ready?'
raw_input()

for page in urlList:
    add_url(page[0], page[1])