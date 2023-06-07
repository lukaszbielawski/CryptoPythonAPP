


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
from model.APIFetcher import APIFetcher

class MainViewModel():
    def __init__(self, view: View, api: APIFetcher):
        self.view = view
        self.update_favourites = False
        self.update_portfolio = False
        self.api = api  # (self, ratio: float, main_vm, api: APIFetcher, table_widget: QTableWidget):
        self.master_viewmodel = master_vm.MasterViewModel(self.view, self, api, self.view.master_table_widget) #default view
        # self.favourites_viewmodel = favourites_vm.FavouritesViewModel(self.view, self, api, self.view.favourites_table)
        # self.portfolio_viewmodel = portfolio_vm.PortfolioViewModel(self.view, self, api, self.view.portfolio_table_widget)
        self.favourites_viewmodel = None
        self.portfolio_viewmodel = None
        self.details_viewmodel = None
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
        if self.favourites_viewmodel is None:
            self.favourites_viewmodel = favourites_vm.FavouritesViewModel(self.view, self, self.api, self.view.favourites_table)
        if self.update_favourites:
            self.update_favourites = False
            print('fupd')
            self.favourites_viewmodel.clearView()
            self.favourites_viewmodel.loadFavourites()
        self.view.stackedWidget.setCurrentIndex(2)

    def myPortfolioButtonClicked(self):
        if self.portfolio_viewmodel is None:
            self.portfolio_viewmodel = portfolio_vm.PortfolioViewModel(self.view, self, self.api, self.view.portfolio_table_widget)
        if self.update_portfolio:
            self.update_portfolio = False
            print('pubd')
            self.portfolio_viewmodel.clearView()
            self.portfolio_viewmodel.loadPortfolio()
        self.view.stackedWidget.setCurrentIndex(3)

    def searchButtonClicked(self):
        print(self.view.tooltip_search_text.text())

    def detailsRequest(self, coin_id):
        print(coin_id, 'main_id')
    
        if self.details_viewmodel is not None:
            self.details_viewmodel.clearView()

        self.details_viewmodel = details_vm.DetailsViewModel(self, self.view, self.api, coin_id)
        self.view.stackedWidget.setCurrentIndex(1)