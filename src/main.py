#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from random import randint
from PyQt5.QtWidgets import QOpenGLWidget
import sys


class Window(QtWidgets.QMainWindow):
    grid1: list
    grid2: list
    map: list

    def __init__(self, parent=None):
        self.g = {'x': 360, 'y': 360}  # Main Window Size
        self.pixNum = {'x': 9, 'y': 9}  # Num of Pixels
        self.pixSize = {
            'x': self.g['x'] / self.pixNum['x'],
            'y': self.g['y'] / self.pixNum['y']
        }  # Size of pixel
        self.grid1 = []
        self.grid2 = []
        self.map = []
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(300, 300, self.g['x'], self.g['y'])
        self.setFixedSize(self.g['x'], self.g['y'])
        self.setWindowTitle('PyQt simple Game')
        self.setWindowIcon(QtGui.QIcon("../assets/icon.jpg"))
        for i in range(self.pixNum['y']):
            self.grid1.append([])
            for j in range(self.pixNum['x']):
                self.grid1[i].append(QtWidgets.QLabel(self))
                self.grid1[i][j].setGeometry(int(i*self.pixSize['x']), int(j*self.pixSize['y']),
                                            int(self.pixSize['x']), int(self.pixSize['y']))
                self.grid1[i][j].setStyleSheet("\
                        border : 1px black; border-style : solid;\
                        background-color: rgba(0,0,0,0);")
        for i in range(self.pixNum['y']):
            self.grid2.append([])
            for j in range(self.pixNum['x']):
                self.grid2[i].append(QtWidgets.QLabel(self))
                self.grid2[i][j].setGeometry(int(i*self.pixSize['x']), int(j*self.pixSize['y']),
                                            int(self.pixSize['x']), int(self.pixSize['y']))
        for i in range(self.pixNum['x']):
            self.map.append([])
            for j in range(self.pixNum['y']):
                if randint(0, 100) >= 50:
                    self.map[i].append("#")
                else:
                    self.map[i].append(".")
        self.updateView(0, 0)
        self.show()

    def updateView(self, x: int, y: int) -> None:  # Update View information
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                if self.map[j][i] == "#":
                    img = QtGui.QPixmap('../assets/floor.png')
                else:
                    img = QtGui.QPixmap('../assets/black.png')
                img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))
                self.grid1[i][j].setPixmap(img)
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                #img = QtGui.QPixmap('../assets/punch3.png')
                img = QtGui.QPixmap()
                img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))
                self.grid2[i][j].setPixmap(img)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()
