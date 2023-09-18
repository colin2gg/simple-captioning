import os
import sys
import typing

import ansicolor
from PIL import Image

import PyQt6
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, Qt, pyqtSignal, QPoint
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QSlider,
    QToolBar,
    QToolButton,
    QFileDialog,
    QStatusBar,
    QWidget
)

def splitTagsString(tags = ""):
    return(tags.replace(', ', ',').split(','))

class IO(object):
    @classmethod
    def warning(cls, message):
        print('WARNING: {}'.format(ansicolor.yellow(str(message))))
    
    @classmethod
    def error(cls, message):
        print('ERROR: {}'.format(ansicolor.red(str(message))))
    
    @classmethod
    def info(cls, message):
        print('INFO: {}'.format(ansicolor.green(str(message))))

class GUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        super(GUI, self).__init__(parent)

        self.setWindowTitle('Simple Captions')

        self.menuDict = self.buildTopBar()
        
    def buildTopBar(self):
        menu = self.menuBar()
        fileMenu = menu.addMenu("File")
        openFolder = fileMenu.addAction("Open Folder")
        return({
             "Menu":menu,
             "FileMenu":fileMenu,
             "OpenFolder":openFolder
                })

class imageBar(QtWidgets.QWidget):

    def __init__(self, parent = None, image = None):
        super(imageBar, self).__init__(parent)
        
        self.imageClass = image
        self.hLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.hLayout)

        self.imageTitle = QtWidgets.QLabel("{} image".format(os.path.basename(self.imageClass.imagePath)))

        self.thumbnailBox = QtWidgets.QPushButton()

        self.tagEdit = QtWidgets.QTextEdit(self.imageClass.returnTagsAsText())
        self.tagEdit.textChanged.connect(self.test)

        self.hLayout.addChildWidget(self.imageTitle)
        #self.hLayout.addChildWidget(self.thumbnailBox)
        self.hLayout.addChildWidget(self.tagEdit)
        self.imageTitle.setBaseSize(256,256)
        IO.info(self.imageTitle.size())
    
    def test(self):
        IO.info("ahhh")

class imageDirectory():
     
    def __init__(self, path):
        # check to make sure directory exists and is valid
        if not os.path.isdir(path):
            IO.error("Image Directory must be used with a directory, not a file")
        if not os.path.exists(path):
            IO.error("Directory does not exist")
        # get directory subfiles
        self.path = path
        self.images = self.createImages()

    def createImages(self):
        imageList = []
        for x in os.listdir(self.path):
            imagePath = os.path.join(self.path, x)
            try:
                Image.open(imagePath)
            except:
                continue
            IO.info(str(x))
            imageList.append(image(imagePath))
        return(imageList)
    


class image():
     
    def __init__(self, path):
        # path | str
        # check if the file path is valid
        if os.path.exists(path) == False:
            raise Exception("image file does not exist")
        
        # get file path and derive the tag path
        self.imagePath = path
        self.tagFile = "{}.txt".format(os.path.splitext(self.imagePath)[0])

        # check for tag file and create one if it's missing
        if not os.path.exists(self.tagFile):
            IO.warning("{} does not have a tag file, creating...".format(os.path.basename(self.imagePath)))
            self.createTagFile()
        
        # log both the image and tag file paths
        IO.info(self.imagePath)
        IO.info(self.tagFile)
    
    def createTagFile(self):
        open(self.tagFile, 'w')
    
    def returnTags(self):
        # returns a list of tags split by ", "
        tags = ""
        if os.path.exists(self.tagFile):
            with open(self.tagFile, 'r') as tf:
                tags = tf.read()
        return(splitTagsString(tags))
    
    def returnTagsAsText(self):
        # returns a list of tags split by ", "
        tags = ""
        if os.path.exists(self.tagFile):
            with open(self.tagFile, 'r') as tf:
                tags = tf.read()
        return(tags)
    
    def addTag(self, tag = "", insertAtStart = False):
        # adds a string tag to either the front or end of the file
        # tag | str
        # insertAtStart | Bool
        if not tag:
            return()

        newtags = splitTagsString(tag)
        currentTags = self.returnTags()
        
        if not currentTags[0] == '':
            if insertAtStart:
                newtags = newtags + currentTags
            else:
                newtags = currentTags + newtags

        seperator = ', '
        tagsAsString = seperator.join(newtags)

        textFile = open(self.tagFile, "w")
        textFile.write(tagsAsString)
    
    def setTags(self, tag = []):
        # overrides the existing tags given a list input
        # tag | list
        seperator = ', '
        tag = seperator.join(tag)
        textFile = open(self.tagFile, 'w')
        textFile.write(tag)

if __name__ == '__main__':
        
    '''
        test2 = imageDirectory("/Users/Shared/TestingFolder/")
        for x in test2.images:
            x.addTag("tag", True)
        
        for x in test2.images:
            IO.info("{}".format(x.returnTags()))
    '''

    newImage = image('/Users/Shared/TestingFolder/download 1.JPG')
    app = QApplication(sys.argv)
    newWidget = imageBar(image = newImage)
    newWidget.show()
    sys.exit(app.exec())