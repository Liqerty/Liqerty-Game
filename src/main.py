from src.UI import Ui_MainWindow
import PyQt5
import sys


class Window(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        PyQt5.QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
