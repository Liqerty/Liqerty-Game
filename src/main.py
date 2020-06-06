#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

if os.getcwd()[-4:] == "/src":
    os.chdir('/'.join(os.getcwd().split("/")[:-1]))  # cross-platform
sys.path.append('/'.join(os.getcwd().split("/")))

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from random import randint
from src.RMC import RMC  # Map generator
from PyQt5.QtWidgets import QOpenGLWidget

class Server:
    ents: list

    def __init__(self):
        self.ents = []

    def addEnt(self, ent: Entity):
        try:
            self.ents.append(ent)
        except:
            print("I don't know why, but I can't add ent to list D:")

    def tick(self):
        for i in range(len(self.ents)):
            try:
                self.ents[i].tick()
            except:
                print("ent["+str(i)+"] can't tick")

    def removeEnt(self, ind):
        try:
            self.ents.pop(ind)
        except:
            print("can't remove ent")

class Entity:
    x: int
    y: int
    live: int

    def __init__(self):
        self.x = 0
        self.y = 0
        self.live = 1

    def move(self, x: int, y: int):
        self.x += x
        self.y += y

    def moveTo(self, x: int, y: int):
        self.x = x
        self.y = y

    def tick(self):
        print(str(self.x)+" YES")

class Enemy(Entity):
    def __init__(self):
        super(Enemy, self).__init__()

class Player(Entity):

    def __init__(self):
        super(Player, self).__init__()
        self.live = 6

    def tick(self):
        pass


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

        self.exit = Entity()
        
        self.newLevel()

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

        # =============== UI ===============
        self.label = QtWidgets.QLabel(self)
        try:
            img = QtGui.QPixmap("assets/life"+str(self.player.live)+".png")
            img = img.scaled(124, 16)
        except:
            img = QtGui.QPixmap("assets/life0.png")
            img = img.scaled(124, 16)
            print("Lives out of range")
        self.label.setPixmap(img)
        self.label.setGeometry(5, 10, 124, 16)
        # ==================================

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

    def newLevel(self):
        self.map = RMC.createMap(60, 120, ".", "#")['grid']

        self.server = Server()
        for i in range(10):
            self.server.addEnt(Enemy())
        self.player = Player()
        for i in range(len(self.map)):
            print(self.map[i])

        self.player.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))
        while self.map[self.player.y][self.player.x] == ".":
            self.player.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))



        self.exit.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))
        while self.map[self.exit.y][self.exit.x] == "." and (self.player.x != self.exit.x or self.player.y != self.exit.y):
            self.exit.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))

    def updateView(self, x: int, y: int) -> None:  # Update View information
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                if len(self.map) > j + y and len(self.map[j]) > i + x and j + y >= 0 and i + x >= 0:
                    if self.map[j + y][i + x] == "#":
                        img = QtGui.QPixmap('assets/floor.png')
                    else:
                        img = QtGui.QPixmap('assets/black.png')
                        if j+y+1 < len(self.map) and j+y-1 >= 0 and\
                                i+x+1 < len(self.map[0]) and i+x-1 >= 0:
                            if self.map[j+y+1][i+x] == "#" or self.map[j+y-1][i+x] == "#" or \
                                    self.map[j+y][i+x+1] == "#" or self.map[j+y][i+x-1] == "#" or \
                                    self.map[j+y+1][i+x+1] == "#" or self.map[j+y+1][i+x-1] == "#" or \
                                    self.map[j+y-1][i+x+1] == "#" or self.map[j+y-1][i+x-1] == "#":
                                img = QtGui.QPixmap('assets/wall1.png')
                else:
                    img = QtGui.QPixmap('assets/black.png')
                img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))
                self.grid1[i][j].setPixmap(img)
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                if self.player.x - x == i and self.player.y - y == j:
                    img = QtGui.QPixmap('assets/wel.png')
                    img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))
                    self.grid2[i][j].setPixmap(img)

        # =============== UI ===============
        try:
            img = QtGui.QPixmap("assets/life" + str(self.player.live) + ".png")
            img = img.scaled(124, 16)
        except:
            pass
        self.label.setPixmap(img)
        self.label.setGeometry(5, 10, 124, 16)
        # ==================================

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_W:
            if self.player.y -1 >= 0:
                if self.map[self.player.y - 1][self.player.x] == "#":
                    self.player.y -= 1
                    self.tick()
        elif e.key() == Qt.Key_S:
            if self.player.y + 1 < len(self.map):
                if self.map[self.player.y + 1][self.player.x] == "#":
                    self.player.y += 1
                    self.tick()
        elif e.key() == Qt.Key_A:
            if self.player.x - 1 >= 0:
                if self.map[self.player.y][self.player.x - 1] == "#":
                    self.player.x -= 1
                    self.tick()
        elif e.key() == Qt.Key_D:
            if self.player.x + 1 < len(self.map[self.player.y]):
                if self.map[self.player.y][self.player.x + 1] == "#":
                    self.player.x += 1
                    self.tick()
        elif e.key() == Qt.Key_Space:
            self.tick()

    def tick(self):
        self.server.tick()
        self.lookAtPlayer()

    def lookAtPlayer(self):
        self.updateView(self.player.x - int(len(self.grid1) / 2), self.player.y - int(len(self.grid1[0]) / 2))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()
