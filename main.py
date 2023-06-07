import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import view.view as view
from view.MainWindow import MainWindow
import viewmodel.main_viewmodel as main_vm
from model.APIFetcher import APIFetcher

class Application(QApplication):
    def __init__(self, args, ratio):
        super(QApplication, self).__init__(args)
        self.window = MainWindow(self)
        self.ratio = ratio
        self.view = view.View(self.ratio, self.window)
        self.api = APIFetcher()
        self.main_viewmodel = main_vm.MainViewModel(self.view, self.api)
        self.run()

    def run(self):
        self.window.show()
        sys.exit(self.exec_())

if __name__ == '__main__':
    ratio = 0.66
    app = Application(sys.argv, ratio)
   
    
    
    