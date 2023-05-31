import sys, os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from master.master_widget import MasterWidget
from ui.navigation_layout import NavigationLayout


class Application(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app