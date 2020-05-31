from src.UI import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnTest.clicked.connect(self.addWidget)

    def addWidget(self):
        test = QtWidgets.QLabel(text="Test", parent=self.centralWidget())
        test.setGeometry(QtCore.QRect(170, 280, 40, 40))
        test.setObjectName("test")
        print(test)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
