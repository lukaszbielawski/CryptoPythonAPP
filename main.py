import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# from main.main_window import MainWindow


class Application(QApplication):
    def __init__(self, args):
        super(QApplication, self).__init__(args)
        self.ui = uic.loadUi('ui/app.ui')
        
        self.ui.show()
        sys.exit(self.exec_())
        

if __name__ == '__main__':
    app = Application(sys.argv)
    # window = MainWindow(app)
    
    # window.show()
    # sys.exit(app.exec_())