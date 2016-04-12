import os
import re
from os import listdir
from PIL import Image

inPath = 'C:\\Fraps\Screenshots'
outPath = 'C:\\Fraps\Screenshots\JPG'
inFormats = r"(^.*\.(bmp|BMP)$)"
outFormat = '.jpg'

def Convert(path):
    if not os.path.exists(inPath):
        print ("Incorrect Path")
        return

    if not os.path.exists(outPath):
        os.makedirs(outPath)

    for fileName in listdir(path):
        if re.search(inFormats, fileName):
            nameWithoutExtension = os.path.splitext(fileName)[0]
            fileNameIn = str(path + '\\' + str(fileName))
            fileNameOut = str(outPath + '\\' + str(nameWithoutExtension) + outFormat)

            image = Image.open(fileNameIn)
            image.save(fileNameOut)

            print("Saved to: " + str(fileNameOut))

Convert(inPath)
input("Finished")