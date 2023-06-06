from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QTableWidget
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
from view.view import View
from viewmodel.listed_viewmodel import ListedViewModel
from model.APIFetcher import APIFetcher
from resources.Constants import ViewModel

class FavouritesViewModel(ListedViewModel):
    def __init__(self, ratio: float, main_vm, api: APIFetcher, table_widget: QTableWidget):
        super().__init__(ratio, main_vm, api, table_widget)
        print('fav init')
        self.api = api
        self.loadFavourites()
        self.setNumberOfFavouriteCoinsValue()

    def loadFavourites(self):
        self.api.fetchListedCoinObjects(ViewModel.FAVOURITES)
        coins = self.api.favourites_coins_array
        try:
            for i in range(len(coins)):
                self.addRow(i, coins[i].id, coins[i].market_cap_rank, coins[i].image, coins[i].name, 
                        coins[i].symbol, coins[i].current_price, coins[i].price_change_percentage_1h_in_currency,
                          coins[i].price_change_percentage_24h_in_currency, coins[i].price_change_percentage_7d_in_currency, 
                          coins[i].total_volume, coins[i].market_cap)
        except Exception as e:
            print(e)


    def setNumberOfFavouriteCoinsValue(self):
        self.view.favourites_number_of_favourite_coins_value.setText(str(len(self.api.favourites_coins_array)))

    def getClickedRow(self, row, column):
        self.main_vm.detailsRequest(self.api.favourites_coins_array[row].id)
    

