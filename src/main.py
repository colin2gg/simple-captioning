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



if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = GUI()
	gui.show()
	sys.exit(app.exec())