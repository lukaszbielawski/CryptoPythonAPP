from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app

        self.__initGeometry()
   

    def __initGeometry(self):
        self.screen = self.app.primaryScreen()
        self.screen_size = self.screen.size()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()