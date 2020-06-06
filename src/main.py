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


class Entity:
    x: int
    y: int
    life: int
    img: QtGui.QPixmap

    def __init__(self, img=None, parent=None):
        if img == None:
            img = QtGui.QPixmap()
        self.x = 0
        self.y = 0
        self.life = 1
        self.img = img
        self.parent = parent

    def move(self, x: int, y: int):
        self.x += x
        self.y += y

    def moveTo(self, x: int, y: int):
        self.x = x
        self.y = y

    def tick(self):
        print(str(self.x) + " " + str(self.x) + " - default ent tick")


class Player(Entity):
    halfLife: int
    fullLife: int
    maxLife: int

    def __init__(self, img=None, parent=None):
        super(Player, self).__init__(img=img, parent=parent)
        self.life = 6
        self.maxLife = 6
        self.halfLife = 0
        self.fullLife = 15

    def tick(self):
        if self.halfLife >= self.fullLife:
            self.halfLife = 0
            if self.life < self.maxLife:
                self.life += 1
        if self.life <= 0:
            self.parent.newLevel()


class Enemy(Entity):
    player: Player
    grid: list

    def __init__(self, player, grid, parent=None, id=None):
        img = QtGui.QPixmap("assets/enemyld.png")
        super(Enemy, self).__init__(img=img, parent=parent)
        self.player = player
        self.grid = grid
        self.id = id

        self.moveTo(randint(0, len(self.grid[0]) - 1), randint(0, len(self.grid) - 1))
        while self.grid[self.y][self.x] == "." and self.player.x != self.x and self.player.y != self.y:
            self.moveTo(randint(0, len(self.grid[0]) - 1), randint(0, len(self.grid) - 1))

    def tick(self):
        if self.x - self.player.x in [-1, 0, 1]:
            if self.y - self.player.y == 0:
                self.player.life -= 1
                self.player.tick()
        if self.y - self.player.y in [-1, 0, 1]:
            if self.x - self.player.x == 0:
                self.player.life -= 1
                self.player.tick()
        if self.life <= 0:
            self.parent.delEnt()


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
                print("ent[" + str(i) + "] can't tick")

    def removeEnt(self, ind):
        try:
            self.ents.pop(ind)
        except:
            print("can't remove ent")


class Window(QtWidgets.QMainWindow):
    grid1: list
    grid2: list
    map: list
    num_of_rooms: int
    player: Player
    server: Server
    exit: Entity

    def __init__(self, parent=None):
        self.g = {'x': 660, 'y': 660}  # Main Window Size
        self.pixNum = {'x': 11, 'y': 11}  # Num of Pixels
        self.pixSize = {
            'x': self.g['x'] / self.pixNum['x'],
            'y': self.g['y'] / self.pixNum['y']
        }  # Size of pixel
        self.grid1 = []
        self.grid2 = []

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

        for i in range(self.pixNum['y']):
            self.grid2.append([])
            for j in range(self.pixNum['x']):
                self.grid2[i].append(QtWidgets.QLabel(self))
                self.grid2[i][j].setGeometry(int(i * self.pixSize['x']), int(j * self.pixSize['y']),
                                             int(self.pixSize['x']), int(self.pixSize['y']))

        # =============== UI ===============
        self.label = QtWidgets.QLabel(self)
        try:
            img = QtGui.QPixmap("assets/life" + str(self.player.life) + ".png")
            img = img.scaled(124, 16)
        except:
            img = QtGui.QPixmap("assets/life0.png")
            img = img.scaled(124, 16)
            print("Lives out of range")
        self.label.setPixmap(img)
        self.label.setGeometry(5, 10, 124, 16)
        # ==================================

        print(self.player.x)
        print(self.player.y)
        self.lookAtPlayer()
        self.show()

    def newLevel(self):
        try:
            del self.player
            del self.exit
            del self.server
            del self.map
            del self.num_of_rooms
        except:
            pass
        mp = RMC.createMap(60, 120, ".", "#")
        self.map = mp['grid']
        self.num_of_rooms = mp['num_of_rooms']
        self.player = Player(QtGui.QPixmap("assets/wel.png").scaled(int(self.pixSize['x']), \
                                                                    int(self.pixSize['y'])), \
                             self)
        self.exit = Entity()
        self.server = Server()
        for i in range(len(self.map)):
            print(self.map[i])
        for i in range(self.num_of_rooms * 10):
            self.server.addEnt(Enemy(self.player, self.map))
        print(self.num_of_rooms)
        self.player.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))
        while self.map[self.player.y][self.player.x] == ".":
            self.player.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))

        self.exit.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))
        while self.map[self.exit.y][self.exit.x] == "." and (
                self.player.x != self.exit.x or self.player.y != self.exit.y):
            self.exit.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))

    def updateView(self, x: int, y: int) -> None:  # Update View information
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                if len(self.map) > j + y and len(self.map[j]) > i + x and j + y >= 0 and i + x >= 0:
                    if self.map[j + y][i + x] == "#":
                        img = QtGui.QPixmap('assets/floor.png')
                    else:
                        img = QtGui.QPixmap('assets/black.png')
                        if j + y + 1 < len(self.map) and j + y - 1 >= 0 and \
                                i + x + 1 < len(self.map[0]) and i + x - 1 >= 0:
                            if self.map[j + y + 1][i + x] == "#" or self.map[j + y - 1][i + x] == "#" or \
                                    self.map[j + y][i + x + 1] == "#" or self.map[j + y][i + x - 1] == "#" or \
                                    self.map[j + y + 1][i + x + 1] == "#" or self.map[j + y + 1][i + x - 1] == "#" or \
                                    self.map[j + y - 1][i + x + 1] == "#" or self.map[j + y - 1][i + x - 1] == "#":
                                img = QtGui.QPixmap('assets/wall1.png')
                else:
                    img = QtGui.QPixmap('assets/black.png')
                img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))
                self.grid1[i][j].setPixmap(img)
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                self.grid2[i][j].clear()
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                for ent in self.server.ents:
                    if ent.x - x == i and ent.y - y == j:
                        img = ent.img
                        img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))
                        self.grid2[i][j].setPixmap(img)
                if self.player.x - x == i and self.player.y - y == j:
                    img = self.player.img
                    self.grid2[i][j].setPixmap(img)

        # =============== UI ===============
        try:
            img = QtGui.QPixmap("assets/life" + str(self.player.life) + ".png")
            img = img.scaled(124, 16)
        except:
            pass
        self.label.setPixmap(img)
        self.label.setGeometry(5, 10, 124, 16)
        # ==================================

    def keyPressEvent(self, e):
        Vec = [0, 0]
        if e.key() == Qt.Key_W:
            if self.player.y - 1 >= 0:
                if self.map[self.player.y - 1][self.player.x] == "#":
                    Vec[1] = -1
        elif e.key() == Qt.Key_S:
            if self.player.y + 1 < len(self.map):
                if self.map[self.player.y + 1][self.player.x] == "#":
                    Vec[1] = 1
        elif e.key() == Qt.Key_A:
            if self.player.x - 1 >= 0:
                if self.map[self.player.y][self.player.x - 1] == "#":
                    Vec[0] = -1
        elif e.key() == Qt.Key_D:
            if self.player.x + 1 < len(self.map[self.player.y]):
                if self.map[self.player.y][self.player.x + 1] == "#":
                    Vec[0] = 1
        elif e.key() == Qt.Key_Space:
            self.player.halfLife += 3
            self.tick()
        if Vec[0] != 0 or Vec[1] != 0:
            can = True
            for ent in self.server.ents:
                if ent.x == self.player.x + Vec[0] and ent.y == self.player.y + Vec[1]:
                    can = False
            if can:
                self.player.move(Vec[0], Vec[1])
                self.player.halfLife += 1
                self.tick()

    def tick(self):
        self.player.tick()
        self.server.tick()
        self.lookAtPlayer()

    def lookAtPlayer(self):
        self.updateView(self.player.x - int(len(self.grid1) / 2), self.player.y - int(len(self.grid1[0]) / 2))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()
