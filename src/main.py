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
    pass

class Entity:
    x: int
    y: int
    life: int
    img: QtGui.QPixmap
    parent: None

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
        if self.life <= 0:
            del self


class Player(Entity):
    stamina: int
    fullStamina: int
    maxLife: int
    damage: int

    def __init__(self, img=None, parent=None):
        super(Player, self).__init__(img=img, parent=parent)
        self.life = 6
        self.maxLife = 6
        self.stamina = 0
        self.fullStamina = 10
        self.damage = 1

    def tick(self):
        if self.stamina >= self.fullStamina:
            if self.life < self.maxLife:
                self.life += 1
                self.stamina = 0
            else:
                self.stamina = self.fullStamina
        if self.life <= 0:
            self.parent.restart()

    def beat(self, x: int, y: int):
        for ent in getattr(self.parent, "server").ents:
            if self.x+x == ent.x and self.y+y == ent.y:
                ent.life -= self.damage


class ServerEnt(Entity):
    server: Server
    spID: int

    def __init__(self, server, img=None, parent=None, spID=None):
        super(ServerEnt, self).__init__(img, parent)
        self.server = server
        self.spID = spID

    def setID(self, spID: int):
        self.spID = spID

    def delMe(self):
        self.parent.server.removeEnt(self.spID)
        self.parent.server.regiveID()


class Enemy(ServerEnt):
    player: Player
    grid: list

    def __init__(self, player, grid, parent=None, spID=None):
        img = QtGui.QPixmap("assets/enemyld.png")
        super(ServerEnt, self).__init__(img=img, parent=parent)
        self.player = player
        self.grid = grid

        self.moveTo(randint(0, len(self.grid[0]) - 1), randint(0, len(self.grid) - 1))
        while self.grid[self.y][self.x] == "." or (self.player.x == self.x and self.player.y == self.y):
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
        if randint(0, 100) > 90:
            tx = randint(self.grid[self.y][self.x-1] == "#", self.grid[self.y][self.x+1] == "#")
            ty = randint(self.grid[self.y-1][tx] == "#", self.grid[self.y+1][tx] == "#")
            self.move(tx, ty)
        if self.life <= 0:
            self.delMe()


class Server:
    ents: list

    def __init__(self):
        self.ents = []

    def addEnt(self, ent: Entity):
        try:
            self.ents.append(ent)
        except:
            print("I don't know why, but I can't add ent to list D:")
        self.regiveID()

    def tick(self):
        for i in range(len(self.ents)):
            try:
                self.ents[i].tick()
            except:
                pass

    def removeEnt(self, ind):
        try:
            self.ents.pop(ind)
        except:
            print("can't remove ent")

    def regiveID(self):
        for i in range(len(self.ents)):
            try:
                self.ents[i].spID = i
            except:
                pass  # Can be Exit



class Exit(Entity):
    player: Player

    def __init__(self, player, img=None, parent=None):
        super(Exit, self).__init__(img=img, parent=parent)
        self.player = player
        self.x = self.player.x
        self.y = self.player.y

    def tick(self):
        if self.x == self.player.x and self.y == self.player.y:
            self.parent.newLevel()


class Window(QtWidgets.QMainWindow):
    grid1: list
    grid2: list
    map: list
    num_of_rooms: int
    player: Player
    server: Server
    exit: Entity

    def __init__(self, parent=None):
        self.started = False
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
        self.setWindowTitle('Liqerty')
        self.setWindowIcon(QtGui.QIcon("assets/icon.png"))
        for i in range(self.pixNum['y']):  # GRID 1
            self.grid1.append([])
            for j in range(self.pixNum['x']):
                self.grid1[i].append(QtWidgets.QLabel(self))
                self.grid1[i][j].setGeometry(int(i * self.pixSize['x']), int(j * self.pixSize['y']),
                                             int(self.pixSize['x']), int(self.pixSize['y']))

        for i in range(self.pixNum['y']):  # GRID 2
            self.grid2.append([])
            for j in range(self.pixNum['x']):
                self.grid2[i].append(QtWidgets.QLabel(self))
                self.grid2[i][j].setGeometry(int(i * self.pixSize['x']), int(j * self.pixSize['y']),
                                             int(self.pixSize['x']), int(self.pixSize['y']))

        # =============== MainMenu ===============
        self.mainMenuLabel = QtWidgets.QLabel(self)
        self.mainMenuImg = QtWidgets.QLabel(self)
        self.mainMenuBtn = QtWidgets.QPushButton(parent=self, text="Start new Game")
        # ========================================

        # =============== UI ===============
        self.lifeUI = QtWidgets.QLabel(self)
        self.staminaUI = QtWidgets.QLabel(self)
        self.lifeUI.setGeometry(5, 10, 124, 16)
        self.staminaUI.setGeometry(5, 25, 124, 6)
        # ==================================
        self.show()
        self.startMainMenu()

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
                             parent=self)
        self.player.life = self.player.maxLife
        self.exit = Exit(self.player, img=QtGui.QPixmap("assets/lestnicha.png"), parent=self)
        self.server = Server()
        self.player.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))
        while self.map[self.player.y][self.player.x] == ".":
            self.player.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))
        for i in range(self.num_of_rooms * 10):
            self.server.addEnt(Enemy(self.player, self.map, parent=self))
        self.server.addEnt(self.exit)

        self.exit.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))
        while self.map[self.exit.y][self.exit.x] == "." and (
                self.player.x != self.exit.x or self.player.y != self.exit.y):
            self.exit.moveTo(randint(0, len(self.map[0]) - 1), randint(0, len(self.map) - 1))

        # self.map = RMC.fillRect(self.map, 0, 0, 10, 10, "#")
        # self.player.x = 0  # Debug room
        # self.player.y = 0
        # self.exit.x = 1
        # self.exit.y = 1

    def updateView(self, x: int, y: int) -> None:  # Update View information
        if not self.started:
            return
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
        img = None
        staminaImg = None
        try:
            img = QtGui.QPixmap("assets/life" + str(self.player.life) + ".png")
            staminaImg = QtGui.QPixmap("assets/stamina (" + str(self.player.stamina+1) + ").png")
            img = img.scaled(124, 16)
            staminaImg = staminaImg.scaled(124, 16)
        except:
            pass
        self.staminaUI.show()
        self.lifeUI.show()
        self.lifeUI.setPixmap(img)
        self.staminaUI.setPixmap(staminaImg)
        self.lifeUI.setGeometry(5, 10, 124, 16)
        self.staminaUI.setGeometry(5, 25, 124, 6)
        # ==================================

    def keyPressEvent(self, e):
        if not self.started:
            return
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
            self.player.stamina += 3
            self.tick()
        if Vec[0] != 0 or Vec[1] != 0:
            can = True
            for ent in self.server.ents:
                if ent.x == self.player.x + Vec[0] and ent.y == self.player.y + Vec[1]:
                    if ent.__class__ != Exit:
                        can = False
            if can:
                self.player.move(Vec[0], Vec[1])
                self.player.stamina += 1
            else:
                self.player.beat(Vec[0], Vec[1])
            self.tick()

    def tick(self):
        self.player.tick()
        self.server.tick()
        self.lookAtPlayer()

    def lookAtPlayer(self):
        self.updateView(self.player.x - int(len(self.grid1) / 2), self.player.y - int(len(self.grid1[0]) / 2))

    def startMainMenu(self):
        self.staminaUI.hide()
        self.lifeUI.hide()
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                img = QtGui.QPixmap("assets/wall1.png")
                if randint(0, 100) > 70:
                    img = QtGui.QPixmap("assets/wall"+str(randint(2, 3))+".png")
                img = img.scaled(int(self.pixSize['x']), int(self.pixSize['y']))
                self.grid2[i][j].setPixmap(img)
        for i in range(self.pixNum['y']):
            for j in range(self.pixNum['x']):
                self.grid1[i][j].clear()
        self.mainMenuLabel.show()
        self.mainMenuImg.show()
        self.mainMenuBtn.show()
        self.mainMenuBtn.setEnabled(True)
        self.mainMenuLabel.setText("Liqerty")
        welcomeImg = QtGui.QPixmap("assets/Welcome.png")
        welcomeImg = welcomeImg.scaled(int(self.g['x']/2), int(self.g['y']/6))
        self.mainMenuImg.setPixmap(welcomeImg)
        self.mainMenuBtn.setText("Start new game")
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(32)
        font.setStyleHint(QtGui.QFont.SansSerif)
        font.setFamily("Source Code Pro")
        self.mainMenuLabel.setStyleSheet("color: #EEE;")
        self.mainMenuLabel.setFont(font)
        self.mainMenuLabel.setGeometry(0, int(self.g['y']/4), self.g['x'], int(self.g['y']/10))
        self.mainMenuImg.setGeometry(0, int(self.g['y']/15), self.g['x'], int(self.g['y']/5))
        self.mainMenuBtn.setGeometry(int(self.g['x']/2-(self.g['x']/10)), int(self.g['y']/15)*8, int(self.g['x']/5), int(self.g['y']/10))
        self.setStyleSheet('''
        QPushButton {
            border:  none;
            border-radius: 5px;
            color: #000; 
            background-color: #fff;
        }
        QPushButton:hover {
            background-color: #aaa;
        }
        ''')  # I hate Qt. Why I need remove border to add color?
        self.mainMenuBtn.clicked.connect(self.start)
        self.mainMenuLabel.setAlignment(Qt.AlignCenter)
        self.mainMenuImg.setAlignment(Qt.AlignCenter)

    def restart(self):
        self.started = False
        self.startMainMenu()

    def start(self):
        if self.started:
            print("WTF?!")
            return
        self.mainMenuLabel.hide()
        self.mainMenuBtn.hide()
        self.mainMenuImg.hide()
        self.mainMenuBtn.setDisabled(True)
        self.started = True
        self.newLevel()
        self.lookAtPlayer()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()
