


import sys, os

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# from view.view import View
from view.view import View
from view.MainWindow import MainWindow
import viewmodel.master_viewmodel as master_vm
import viewmodel.favourites_viewmodel as favourites_vm
import viewmodel.details_viewmodel as details_vm
import viewmodel.portfolio_viewmodel as portfolio_vm

class MainViewModel():
    def __init__(self, view):
        self.view = view
        self.toUpdate = True
        self.master_viewmodel = master_vm.MasterViewModel(self.view, self) #default view
        self.favourites_viewmodel = favourites_vm.FavouritesViewModel(self.view, self)
        self.portfolio_viewmodel = portfolio_vm.PortfolioViewModel(self.view, self)
        self.__connectButtons()
        
    def __connectButtons(self):
        self.view.quit_button.clicked.connect(self.view.window.close)
        self.view.main_button.clicked.connect(lambda: self.mainButtonClicked())
        self.view.favourites_button.clicked.connect(lambda: self.favouritesButtonClicked())
        self.view.my_portfolio_button.clicked.connect(lambda: self.myPortfolioButtonClicked())
        self.view.tooltip_search_button.clicked.connect(lambda: self.searchButtonClicked())

    def mainButtonClicked(self):
        self.view.stackedWidget.setCurrentIndex(0)

    def favouritesButtonClicked(self):
        if self.toUpdate:
            self.favourites_viewmodel = favourites_vm.FavouritesViewModel(self.view, self)
        self.view.stackedWidget.setCurrentIndex(2)

    def myPortfolioButtonClicked(self):
        if self.toUpdate:
            self.portfolio_viewmodel = portfolio_vm.PortfolioViewModel(self.view, self)
        self.view.stackedWidget.setCurrentIndex(3)

    def searchButtonClicked(self):
        print(self.view.tooltip_search_text.text())

    def detailsRequest(self):
        self.details_viewmodel = details_vm.DetailsViewModel(self.view)
        self.view.stackedWidget.setCurrentIndex(1)