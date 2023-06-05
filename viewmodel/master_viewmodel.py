from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import view.view as view
import viewmodel.details_viewmodel as details_vm
from model.APIFetcher import APIFetcher
from model.coins_utils import ListedCoinObject, CoinLogoWidget
import urllib, threading, io, os
import urllib.request
from urllib.request import Request
import PIL, math
from resources.Constants import Color, ViewModel
from viewmodel.abstract_viewmodel import ListedViewModel

class MasterViewModel(ListedViewModel):
    def __init__(self, view: view.View, main_vm, api: APIFetcher):
        print('master init')
        self.view = view
        self.main_vm = main_vm
        self.api = api
        self.row_count = 0
        self.readyToScroll = True
        self.already_loaded = 0
        self.per_page = 40
        # self.setMarketCapSuffixLabel(1.21, -7.0)
        # self.setMarketCapWidgetValue('$931,333,754,362')
        # self.setTradingVolumeWidgetValue('$31,333,754,362')
        # self.setBtcDominanceWidgetValue('43.5%')
        # self.setNumberOfCoinsValue(500)
        self.__initFont()
        self.__cfgTable()
        self.loadGlobalStats()
        self.loadPage()
        # self.loadPage(100)

    def onMasterTableScroll(self, *args):
        rect = self.view.master_table_widget.viewport().rect()
        # top_index = self.view.master_table_widget.indexAt(rect.topLeft()).row()
        bottom_index = self.view.master_table_widget.indexAt(rect.bottomLeft()).row()
        print(bottom_index, self.already_loaded)
        if bottom_index + 1 == self.already_loaded and self.readyToScroll:
            self.readyToScroll = False
            self.loadPage()
            self.readyToScroll = True
            # self.unloadPage(top_index)
        # elif top_index <= 50 and self.readyToScroll:
        #     self.readyToScroll = False
        #     # self.loadPage(100 * (self.loads -)
        #     self.unloadPage(top_index)
        #     self.readyToScroll = True
            



    # def unloadPage(self, top_index):
    #     self.loads -= 1
    #     for _ in range(100):
    #         self.view.master_table_widget.removeRow(0)
    #     self.view.master_table_widget.verticalScrollBar().setValue(top_index - 100)
        

    def loadPage(self):
        print(self.already_loaded + self.per_page > self.api.get_coins_loaded())
        if self.already_loaded + self.per_page > self.api.get_coins_loaded():
            self.api.fetchListedCoinObjects(ViewModel.MASTER)
        try:
            coins = self.api.master_coins_array
            for i in range(self.per_page):
                # self.addRow(i + offset, int(self.row_count + 1), './resources/logo.png', 'Bitcoin', 'BTC', '$26,961.43', '-0.1%', '-2.6%', '+2.4%', '$16,332,763,917', '$522,840,485,971')
                self.addRow(self.already_loaded + i, coins[self.already_loaded + i].id, coins[self.already_loaded + i].market_cap_rank, coins[self.already_loaded + i].image, coins[self.already_loaded + i].name, 
                        coins[self.already_loaded + i].symbol, coins[self.already_loaded + i].current_price, coins[self.already_loaded + i].price_change_percentage_1h_in_currency,
                          coins[self.already_loaded + i].price_change_percentage_24h_in_currency, coins[self.already_loaded + i].price_change_percentage_7d_in_currency, 
                          coins[self.already_loaded + i].total_volume, coins[self.already_loaded + i].market_cap)
            self.already_loaded += self.per_page
        except Exception as e:
            print(e)

    def loadGlobalStats(self):
        global_data = self.api.global_data
        self.setMarketCapSuffixLabel(int(global_data.total_market_cap), global_data.market_cap_change_percentage_24h)
        self.setMarketCapWidgetValue('${:,}'.format(int(global_data.total_market_cap)))
        self.setTradingVolumeWidgetValue('${:,}'.format(int(global_data.total_volume)))
        self.setBtcDominanceWidgetValue(str(self._format_percentage(global_data.btc_dominance)) + '%')
        self.setNumberOfCoinsValue('{:,}'.format(global_data.active_cryptocurrencies))


    def _format_percentage(self, percent):
        try:
            return round(percent, 1)
        except Exception as e:
            print(e)
            return '—'
        
    def __convert_number_to_written(self, number):
        digits = int(math.log10(number))
        number = str(number)
        
        if digits in {9, 10, 11}:
            name = ' Billion'
            string = number[:digits - 7]
            string_with_dot = string[:digits - 8] + '.' + string[digits - 8:]
        else:
            string = number[:digits - 10]
            string_with_dot = string[:digits - 11] + '.' + string[digits - 11:]
            name = ' Trillion'
        return string_with_dot + name
        

        
        
    def setMarketCapSuffixLabel(self, value, change):
        if change >= 0:
            self.view.market_cap_suffix_label.setText(f'{self.__convert_number_to_written(value)}, a <font color=#54EE1F>{self._format_percentage(change)}%</font> increase in the last 24 hours.')
        else:
            self.view.market_cap_suffix_label.setText(f'{self.__convert_number_to_written(value)}, a <font color=#F0302C>{self._format_percentage(change)}%</font> decrease in the last 24 hours.')
    
    def setMarketCapWidgetValue(self, value):
        self.view.market_cap_widget_value.setText(str(value))

    def setTradingVolumeWidgetValue(self, value):
        self.view.trading_volume_widget_value.setText(str(value))

    def setBtcDominanceWidgetValue(self, value):
        self.view.btc_dominance_widget_value.setText(str(value))

    def setNumberOfCoinsValue(self, value):
        self.view.number_of_coins_widget_value.setText(str(value))

    def getClickedRow(self, row, column):
        self.main_vm.detailsRequest(self.api.master_coins_array[row].id)
        print(row) 


