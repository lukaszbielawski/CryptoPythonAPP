import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from ui.ui import Ui_Form
# from ui.ui_half import Ui_Form

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
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(app)
    ratio = 0.5
    ui = Ui_Form(ratio)
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
    