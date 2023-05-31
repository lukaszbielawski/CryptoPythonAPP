import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from view.view import View
from view.MainWindow import MainWindow
from viewmodel.master_viewmodel import MasterViewModel
  
class Application(QApplication):
    def __init__(self, args):
        super(QApplication, self).__init__(args)
        self.window = MainWindow(self)
        self.ratio = 0.5
        self.view = View(self.ratio, self.window, self)
        self.view.setupUi(self.window)
        self.__initViewModels()
        self.run()

    def __initViewModels(self):
        self.master_viewmodel = MasterViewModel(self.view)
    
    def run(self):
        self.window.show()
        sys.exit(self.exec_())

if __name__ == '__main__':
    app = Application(sys.argv)
   
    
    
    