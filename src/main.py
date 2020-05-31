#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  =================================
#   Name: Simple PyQt-Game
#   Author: Liqerty team
#   Description: RougeLike
#  =================================

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QOpenGLWidget
import sys


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.g = {'x': 400, 'y': 400}
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(300, 300, self.g['x'], self.g['y'])
        self.setWindowTitle('OpenGL simple Game')
        self.setWindowIcon(QtGui.QIcon("../assets/icon.jpg"))

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()
