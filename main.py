import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication
import view.view as view
from view.MainWindow import MainWindow
import viewmodel.main_viewmodel as main_vm
from model.APIFetcher import APIFetcher

class Application(QApplication):
    #This custom class contains running application
    def __init__(self, args, ratio):
        #This app's constructor creates needed components for application to work properly
        super(QApplication, self).__init__(args)
        self.window = MainWindow(self)
        self.ratio = ratio
        self.view = view.View(self.ratio, self.window)
        self.api = APIFetcher()
        self.main_viewmodel = main_vm.MainViewModel(self.view, self.api)
        self.run()

    def run(self):
        #This method show window and runs the app
        self.window.show()
        sys.exit(self.exec_())

if __name__ == '__main__':
    ratio = 1
    #Screen ratio value is needed to display views in proper scale
    app = Application(sys.argv, ratio)
   
    
    
    