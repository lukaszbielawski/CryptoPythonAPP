import sys, os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from master.master_widget import MasterWidget
from ui.navigation_layout import NavigationLayout


class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app

        self.__initGeometry()
        self.__initStyle(bg_color='#171717')
        
        self.main_layout = QVBoxLayout()
        self.navigation_layout = NavigationLayout()
       
        # self.current_widget = MasterWidget(self)
        self.main_layout.addLayout(self.navigation_layout)
        self.main_layout.addStretch(1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        
        self.setCentralWidget(self.central_widget)


   

    def __initGeometry(self):
        self.screen = self.app.primaryScreen()
        self.screen_size = self.screen.size()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(int(self.screen_size.width() * 0.125), 0, int(self.screen_size.width() * 0.75), int(self.screen_size.height() * 0.75)) 

    def __initStyle(self, bg_color):
        self.setStyleSheet(f"background-color: {bg_color};")

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()