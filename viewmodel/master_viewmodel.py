from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QTableWidget
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import view.view as view
import viewmodel.details_viewmodel as details_vm
from model.APIFetcher import APIFetcher
import model.coins_utils as utils
import urllib, threading, io, os
import urllib.request
from urllib.request import Request
import PIL, math
from resources.Constants import Color, ViewModel
from viewmodel.listed_viewmodel import ListedViewModel

class MasterViewModel(ListedViewModel):
    def __init__(self, ratio: float, main_vm, api: APIFetcher, table_widget: QTableWidget):
        super().__init__(ratio, main_vm, api, table_widget)
        self.table_widget.verticalScrollBar().valueChanged.connect(self.onMasterTableScroll)
        self.readyToScroll = True
        self.already_loaded = 0
        self.per_page = 40
        self.loadGlobalStats()
        self.loadPage()

    def onMasterTableScroll(self, *args):
        rect = self.view.master_table_widget.viewport().rect()
        # top_index = self.view.master_table_widget.indexAt(rect.topLeft()).row()
        bottom_index = self.view.master_table_widget.indexAt(rect.bottomLeft()).row()
        if bottom_index + 1 == self.already_loaded and self.readyToScroll:
            self.readyToScroll = False
            self.loadPage()
            self.readyToScroll = True

    def loadPage(self):
        if self.already_loaded + self.per_page > self.api.get_coins_loaded():
            self.api.fetchListedCoinObjects(ViewModel.MASTER)
        try:
            coins = self.api.master_coins_array
            for i in range(self.per_page):
                self.addRow(self.already_loaded + i, coins[self.already_loaded + i].id, coins[self.already_loaded + i].market_cap_rank, coins[self.already_loaded + i].image, coins[self.already_loaded + i].name, 
                        coins[self.already_loaded + i].symbol, coins[self.already_loaded + i].current_price, coins[self.already_loaded + i].price_change_percentage_1h_in_currency,
                          coins[self.already_loaded + i].price_change_percentage_24h_in_currency, coins[self.already_loaded + i].price_change_percentage_7d_in_currency, 
                          coins[self.already_loaded + i].total_volume, coins[self.already_loaded + i].market_cap)
            self.already_loaded += self.per_page
        except Exception as e:
            print(e)

    def loadGlobalStats(self):
        global_data = self.api.global_data
        self.setMarketCapSuffixLabel(global_data.total_market_cap, global_data.market_cap_change_percentage_24h)
        self.setMarketCapWidgetValue(global_data.total_market_cap)
        self.setTradingVolumeWidgetValue(global_data.total_volume)
        self.setBtcDominanceWidgetValue(global_data.btc_dominance)
        self.setNumberOfCoinsValue(global_data.active_cryptocurrencies)
        
    def setMarketCapSuffixLabel(self, value, change):
        if change >= 0:
            self.view.market_cap_suffix_label.setText(f'{utils.convert_number_to_written(value)}, a <font color={Color.GREEN.value}>{utils.format_percentage(change)}</font> increase in the last 24 hours.')
        else:
            self.view.market_cap_suffix_label.setText(f'{utils.convert_number_to_written(value)}, a <font color={Color.RED.value}>{utils.format_percentage(change)}</font> decrease in the last 24 hours.')
    
    def setMarketCapWidgetValue(self, value):
        self.view.market_cap_widget_value.setText(utils.format_big_price(value))

    def setTradingVolumeWidgetValue(self, value):
        self.view.trading_volume_widget_value.setText(utils.format_big_price(value))

    def setBtcDominanceWidgetValue(self, value):
        self.view.btc_dominance_widget_value.setText(utils.format_percentage(value))

    def setNumberOfCoinsValue(self, value):
        self.view.number_of_coins_widget_value.setText(utils.format_number(value))

    def getClickedRow(self, row, column):
        self.main_vm.detailsRequest(self.api.master_coins_array[row].id)


