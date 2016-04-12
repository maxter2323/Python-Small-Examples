import sys
import ctypes
import re
from os import listdir
from tkinter import *
from tkinter import  filedialog
from PIL import Image, ImageTk

class App(Frame):

    def __init__(self, master):
        self.root = master
        Frame.__init__(self, master, relief=GROOVE,width=root['width'],height=root['height'])

        self.filenames = []
        self.originals = []
        self.images = []
        self.buttons = []
        self.frameHeight = 600
        self.imageSize = (128, 72)

        self.scrollStart = 0
        self.scrollEnd = 0

        self.placeHolderOriginal = Image.new("RGB", self.imageSize, (31,174,222))
        self.placeHolderResized = self.placeHolderOriginal.resize(self.imageSize, Image.ANTIALIAS)
        self.placeHolder = ImageTk.PhotoImage(self.placeHolderResized)

        self.display = Canvas(self, bd=0, highlightthickness=0, width=root['width'],height=root['height'])
        self.frame=Frame(self.display)
        self.myscrollbar=Scrollbar(self,orient="vertical")
        self.myscrollbar.config(command=self.display.yview)

        self.initUI()
        self.update()

    def update(self):
        equalsStart = (self.scrollStart == self.myscrollbar.get()[0])
        equalsEnd = (self.scrollEnd == self.myscrollbar.get()[1])

        if equalsStart==False or equalsEnd==False:
            self.adjustImages()

        self.after(33, self.update)

    #*******************************************************************************************************
    #                                           TKINTER METHODS
    #*******************************************************************************************************

    def initUI(self):
        self.display.configure(yscrollcommand=self.myscrollbar.set)

        self.myscrollbar.pack(side="right",fill="y")
        self.display.pack(side="left")

        self.display.create_window((0,0),window=self.frame,anchor='nw')
        self.frame.bind("<Configure>", self.configureFrame)

        self.pack(fill=BOTH, expand=1)
        self.bind("<Configure>", self.resize)

        self.makeMenuButtons()

    def configureFrame(self, event):
        self.display.configure(scrollregion= self.display.bbox("all"),width=self.frame.winfo_width(),height=self.frame.winfo_height())

    def resize(self, event):
        self.resizeCustom(event.width, event.height)

    def getVisibleArea(self):
        self.scrollStart = self.myscrollbar.get()[0]
        self.scrollEnd = self.myscrollbar.get()[1]
        startY = self.frameHeight * self.scrollStart
        endY = self.frameHeight * self.scrollEnd
        return  startY, endY;

    def makeMenuButtons(self):
        menubar = Menu(self.root)
        menubar.add_command(label="Open Folder", command=self.askDirectory)
        self.root.config(menu=menubar)

    #*******************************************************************************************************
    #                                           DATA METHODS
    #*******************************************************************************************************

    def getFilenames(self, path):
        self.filenames = []
        fileNames = [f for f in listdir(path)]
        regex = r"(^.*\.(jpg|JPG|png|PNG|bmp|BMP)$)"
        for fileName in fileNames:
            if re.search(regex, fileName):
                self.filenames.append(path + '\\' + str(fileName))

    def loadOriginal(self, path):
        original = Image.open(path)
        resized = original.resize(self.imageSize, Image.ANTIALIAS)
        return resized

    def makeImageFromOriginal(self, original):
        image = ImageTk.PhotoImage(original)
        return image

    def loadImages(self):
        self.images = []
        self.originals = []
        for filename in self.filenames:
            original = self.loadOriginal(filename)
            self.originals.append(original)
            image = self.makeImageFromOriginal(original)
            self.images.append(image)

    def makeButtons(self):
        self.buttons = []
        for filename in self.filenames:
            button = Button(self.frame, image=self.placeHolder, width=self.imageSize[0], height=self.imageSize[1])
            buttonMethod= lambda j=filename: self.changeWallpaper(j)
            button.configure(command=buttonMethod)
            self.buttons.append(button)

    def clearAll(self):
        del self.filenames[:]
        for b in self.buttons:
            b.grid_forget()
            b.destroy()
        del self.buttons[:]
        self.display.grid_forget()
        self.frame.grid_forget()
        del self.images[:]
        del self.originals[:]

    def loadAll(self, path):
        if path == '':
            return
        self.clearAll()
        self.getFilenames(path)
        self.loadImages()
        self.makeButtons()
        self.resizeCustom(self.display.winfo_width(), self.display.winfo_height())

    #*******************************************************************************************************
    #                                           FUNCTIONAL METHODS
    #*******************************************************************************************************

    def askDirectory(self):
        optionsd = {}
        optionsd['initialdir'] = 'C:\\'
        optionsd['mustexist'] = False
        optionsd['parent'] = self.root
        optionsd['title'] = 'This is a title'
        return self.loadAll(filedialog.askdirectory(**optionsd))

    def changeWallpaper(self, image_path):
        SPI_SETDESKWALLPAPER = 0x14     #command (20)
        SPIF_UPDATEINIFILE   = 0x2      #forces instant update
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE)

    #*******************************************************************************************************
    #                                           RESIZE METHODS
    #*******************************************************************************************************

    def resizeCustom(self, windowWidth, windowHeight):
        self.adjustButtons(windowWidth)
        self.adjustImages()

    def adjustButtons(self, windowWidth):
        column = 0
        row = 0
        currentX = 0
        for b in self.buttons:
            b.configure(width=self.imageSize[0], height=self.imageSize[1])
            b.grid(row=row,column=column)

            bWidth = b.winfo_width()
            currentX+=bWidth
            column+=1
            if currentX + bWidth>= windowWidth:
                    row += 1
                    column = 0
                    currentX = 0

        self.frameHeight = (row + 1) * self.imageSize[1]

    def adjustImages(self):
        visibleArea = self.getVisibleArea()
        for i in range(len(self.buttons)):
            b = self.buttons[i]
            bY = b.winfo_y()

            if bY + self.imageSize[1] < visibleArea[0] or bY > visibleArea[1]:
                self.images[i] = self.placeHolder
                b.configure(image=self.placeHolder)
            else:
                if self.images[i] == self.placeHolder:
                    self.images[i] = self.makeImageFromOriginal(self.originals[i])
                    b.configure(image=self.images[i])

root = Tk()
root.wm_geometry("%dx%d+%d+%d" % (800, 600, 300, 200))

app = App(root)
app.loadAll('C:\\images')

app.mainloop()