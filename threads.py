import random
import threading
import time
import os
import urllib.request
import urllib.parse
import urllib.error

maxId = 364924
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
    'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://alpha.wallhaven.cc/',
    'Cookie': '__cfduid=dda3304d00174cf30a6e5fbde97f14bf21460841452',
    'Connection': 'keep-alive'
}
linkbody = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-{number}.jpg'

def saveImage(filename, foldername, content):
    if content == None:
        print("Failed to load url in Thread " + foldername[len(foldername)- 2] )
        return
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    f = open(filename + '.jpg', 'wb')
    f.write(content.read())
    f.close()
    global loadedAmount
    loadedAmount += 1
    print("Saved: " + filename)

def loadImage():
    number = random.randrange(0, maxId)
    url = linkbody.format(number=number)
    request = urllib.request.Request(url, data=None, headers=headers)
    try:
        content = urllib.request.urlopen(request)
    except urllib.error.HTTPError:
        return
    return  content

def donwloadMethod(folderName, count):
    nameBase = 'Assets/' + folderName + '/'
    for i in range(count):
        filename = nameBase + str(i)
        image = loadImage()
        saveImage(filename, nameBase, image)
    print("Finished: Thread " + folderName)

def makeThread(name, imagesToLoad):
    thread = threading.Thread(target=donwloadMethod, args=(name, imagesToLoad))
    return thread

threadAmount = 8
imagesToLoad = 3
threads = []
loadedAmount = 0
estimatedAmount = threadAmount * imagesToLoad

for i in range(threadAmount):
    thread = makeThread(str(i+1), imagesToLoad)
    threads.append(thread)

start = time.time()

for j in range(threadAmount):
    threads[j].start()

for k in range(threadAmount):
    threads[k].join()

end = time.time()
print("Time: " + str(end - start))
print("Total images loaded: " + str(loadedAmount) + '/' + str(estimatedAmount))