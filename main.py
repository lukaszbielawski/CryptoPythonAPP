import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from resources.ui import Ui_Form

class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app

        self.__initGeometry()

   

    def __initGeometry(self):
        self.screen = self.app.primaryScreen()
        self.screen_size = self.screen.size()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(int(self.screen_size.width() * 0.125), 0, int(self.screen_size.width() * 0.75), int(self.screen_size.height() * 0.75)) 
        
    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(app)
    ui = Ui_Form()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
    