import os
import sys
import typing

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
     
     def __init__(self):
          pass

class image():
     
    def __init__(self, path):
        

        if os.path.exists(path) == False:
            raise Exception("image file does not exist")
        
        self.imagePath = path
        self.tagFile = "{}.txt".format(os.path.splitext(self.imagePath)[0])
        self.hasTagFolder = os.path.exists(self.tagFile)
        print (self.imagePath)
        print (self.tagFile)
        print (self.hasTagFolder)
    
    def createTagFile(self):
        with open(self.tagFile, 'w') as fp:
            pass
    
    def returnTags(self):
        tags = ""
        if os.path.exists(self.tagFile):
            with open(self.tagFile, 'r') as tf:
                tags = tf.read()
        return(tags.split(', '))
    
    def addTag(self, tag = "", insertAtStart = False):
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
        seperator = ', '
        tag = seperator.join(tag)
        textFile = open(self.tagFile, 'w')
        textFile.write(tag)

if __name__ == '__main__':
    test = image("/Users/grettaklu/Desktop/profileEmi--1.jpg")
    test.createTagFile()
    test.addTag("test")
    test.addTag("after test")
    test.addTag("before test", True)
    print (test.returnTags())
    test.setTags(['new before', 'new test', 'new after'])
    print (test.returnTags())
    
    '''
    app = QApplication(sys.argv)
	gui = GUI()
	gui.show()
	sys.exit(app.exec())
    '''