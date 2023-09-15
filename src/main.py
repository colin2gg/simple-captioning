import os
import sys
import typing

import ansicolor

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

    def __init__(self, parent = None    ):
        super(GUI, self).__init__(parent)

        self.setWindowTitle('Image Caption')

        self.menuDict = self.buildTopBar()
        
    def buildTopBar(self):
        menu = self.menuBar()
        fileMenu = menu.addMenu("File")
        openFolder = fileMenu.addAction("Open Folder")
        return({
             "Menu":menu,
             "FileMenu":fileMenu,
             "openFolder":openFolder
                })

class tagger():
     
    def __init__(self, path):
        pass

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
        return(tags.split(', '))
    
    def addTag(self, tag = "", insertAtStart = False):
        # adds a string tag to either the front or end of the file
        # tag | str
        # insertAtStart | Bool
        if not tag:
            return()

        newtags = tag.split(', ')
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
    test = image("")    
    
    IO.info("")
    IO.info("Running Test A: ")
    test.addTag("test")
    test.addTag("after test")
    test.addTag("before test", True)
    IO.info(test.returnTags())

    if test.returnTags() == ['before test', 'test', 'after test']:
        IO.info("Test A Passed")
    else:
        IO.error("Test A Failed")

    IO.info("")
    IO.info("Running Test B: ")
    test.setTags(['new before', 'new test', 'new after'])
    IO.info(test.returnTags())
    if test.returnTags() == ['new before', 'new test', 'new after']:
        IO.info("Test B Passed")
    else:
        IO.error("Test B Failed")


    '''
    app = QApplication(sys.argv)
	gui = GUI()
	gui.show()
	sys.exit(app.exec())
    '''