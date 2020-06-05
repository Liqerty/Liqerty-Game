#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

print(os.getcwd())
if os.getcwd()[-4:] == "/src":
    os.chdir('/'.join(os.getcwd().split("/")[:-1]))  # cross-platform
print(os.getcwd())
sys.path.append('/'.join(os.getcwd().split("/")))
print(sys.path)

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from random import randint
from src.RMC import RMC  # Map generator
from PyQt5.QtWidgets import QOpenGLWidget


class Entity:
    x: int
    y: int

    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, x: int, y: int):
        self.x += x
        self.y += y

    def moveTo(self, x: int, y: int):
        self.x = x
        self.y = y


class Player(Entity):

    def __init__(self):
        super().__init__()


class Window(QtWidgets.QMainWindow):
    grid1: list
    grid2: list
    map: list
    player: Player

    def __init__(self, parent=None):
        self.g = {'x': 660, 'y': 660}  # Main Window Size
        self.pixNum = {'x': 11, 'y': 11}  # Num of Pixels
        self.pixSize = {
            'x': self.g['x'] / self.pixNum['x'],
            'y': self.g['y'] / self.pixNum['y']
        }  # Size of pixel
        self.grid1 = []
        self.grid2 = []
        self.map = RMC.createMap(120, 120, ".", "#")['grid']
        self.player = Player()
        for i in range(len(self.map)):
            print(self.map[i])

        self.player.moveTo(randint(0, len(self.map) - 1), randint(0, len(self.map[0]) - 1))
        while self.map[self.player.y] == "." or \
                self.map[self.player.y][self.player.x] == ".":
            self.player.moveTo(randint(0, len(self.map) - 1), randint(0, len(self.map[0]) - 1))

        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(300, 200, self.g['x'], self.g['y'])
        self.setFixedSize(self.g['x'], self.g['y'])
        self.setWindowTitle('PyQt simple Game')
        self.setWindowIcon(QtGui.QIcon("assets/icon.jpg"))
        for i in range(self.pixNum['y']):
            self.grid1.append([])
            for j in range(self.pixNum['x']):
                self.grid1[i].append(QtWidgets.QLabel(self))
                self.grid1[i][j].setGeometry(int(i * self.pixSize['x']), int(j * self.pixSize['y']),
                                             int(self.pixSize['x']), int(self.pixSize['y']))
        for i in range(self.pixNum['y']):
            self.grid2.append([])
            for j in range(self.pixNum['x']):
                self.grid2[i].append(QtWidgets.QLabel(self))
                self.grid2[i][j].setGeometry(int(i * self.pixSize['x']), int(j * self.pixSize['y']),
                                             int(self.pixSize['x']), int(self.pixSize['y']))
        print(self.player.x)
        print(self.player.y)
        self.lookAtPlayer()
        self.show()

    def updateView(self, x: int, y: int) -> None:  # Update View information
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                if len(self.map) > j + y and len(self.map[j]) > i + x and j + y >= 0 and i + x >= 0:
                    if self.map[j + y][i + x] == "#":
                        img = QtGui.QPixmap('assets/floor.png')
                    else:
                        if self.map[j+y+1][i+x] == "#" or self.map[j+y-1][i+x] == "#" or \
                                self.map[j+y][i+x+1] == "#" or self.map[j+y][i+x-1] == "#" or \
                                self.map[j+y+1][i+x+1] == "#" or self.map[j+y+1][i+x-1] == "#" or \
                                self.map[j+y-1][i+x+1] == "#" or self.map[j+y-1][i+x-1] == "#":
                            img = QtGui.QPixmap('assets/wall1.png')
                        else:
                            img = QtGui.QPixmap('assets/black.png')
                else:
                    img = QtGui.QPixmap('assets/wall1.png')
                img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))
                self.grid1[i][j].setPixmap(img)
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                # img = QtGui.QPixmap('assets/punch3.png')
                if self.player.x - x == i and self.player.y - y == j:
                    img = QtGui.QPixmap('assets/wel.png')
                    img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))
                    self.grid2[i][j].setPixmap(img)
                # else:
                #    img = QtGui.QPixmap("")
                #    img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_W:
            if self.map[self.player.y - 1][self.player.x] == "#":
                self.player.y -= 1
                self.tick()
        elif e.key() == Qt.Key_S:
            if self.map[self.player.y + 1][self.player.x] == "#":
                self.player.y += 1
                self.tick()
        elif e.key() == Qt.Key_A:
            if self.map[self.player.y][self.player.x - 1] == "#":
                self.player.x -= 1
                self.tick()
        elif e.key() == Qt.Key_D:
            if self.map[self.player.y][self.player.x + 1] == "#":
                self.player.x += 1
                self.tick()
        elif e.key() == Qt.Key_Space:
            self.tick()

    def tick(self):
        self.lookAtPlayer()

    def lookAtPlayer(self):
        self.updateView(self.player.x - int(len(self.grid1) / 2), self.player.y - int(len(self.grid1[0]) / 2))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()
