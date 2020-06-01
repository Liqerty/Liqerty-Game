#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QOpenGLWidget
import sys


class Window(QtWidgets.QMainWindow):
    grid: list

    def __init__(self, parent=None):
        self.g = {'x': 400, 'y': 400}  # Main Window Size
        self.pixNum = {'x': 10, 'y': 10}  # Num of Pixels
        self.pixSize = {
            'x': self.g['x'] / self.pixNum['x'],
            'y': self.g['y'] / self.pixNum['y']
        }  # Size of pixel
        self.grid = []
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(300, 300, self.g['x'], self.g['y'])
        self.setWindowTitle('OpenGL simple Game')
        self.setWindowIcon(QtGui.QIcon("../assets/icon.jpg"))
        for i in range(self.pixNum['y']):
            self.grid.append([])
            for j in range(self.pixNum['x']):
                self.grid[i].append(QtWidgets.QLabel(self))
                self.grid[i][j].setGeometry(int(i*self.pixSize['x']), int(j*self.pixSize['y']),
                                            int(self.pixSize['x']), int(self.pixSize['y']))
                self.grid[i][j].setStyleSheet("border : 1px black; border-style : solid; background-color: #ccc")
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()
