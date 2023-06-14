from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    # A custom class which represents application's window.
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #This method removes frame from application's window.

    def mousePressEvent(self, event):
        #Called everytime user presses left mouse button.
        self.oldPosition = event.globalPos()
        

    def mouseMoveEvent(self, event):
        #Called everytime user moves mouse.
        delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()
        #This is made to move window via click & drag beacuse by default after you remove frame you cannot move window around freely anymore.