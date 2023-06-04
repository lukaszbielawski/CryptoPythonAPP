import string, decimal, threading
import numpy as np
import urllib
from urllib.request import Request
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt

class ListedCoinObject():
    def __init__(self, id, market_cap_rank, image, name, symbol, current_price, 
                 price_change_percentage_1h_in_currency, price_change_percentage_24h_in_currency, 
                 price_change_percentage_7d_in_currency, total_volume, market_cap):
        self.id = id
        self.market_cap_rank = market_cap_rank
        self.image = image
        self.name = name
        self.symbol = symbol.upper()
        self.current_price = self.__format_currency(current_price)
        self.price_change_percentage_1h_in_currency = self.__format_percentage(price_change_percentage_1h_in_currency)
        self.price_change_percentage_24h_in_currency = self.__format_percentage(price_change_percentage_24h_in_currency)
        self.price_change_percentage_7d_in_currency = self.__format_percentage(price_change_percentage_7d_in_currency)
        self.total_volume = total_volume
        self.market_cap = market_cap
        
    def __format_currency(self, currency):
        try:
            sci_currency = "{:.3e}".format(currency)
            number = decimal.Decimal(sci_currency)
            return number
        except Exception as e:
            print(e)
            return 0.0
        
    def __format_percentage(self, percent):
        try:
            return round(percent, 1)
        except Exception as e:
            print(e)
            return '—'
    
    
    
               
          