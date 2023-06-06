import string, decimal, datetime
import numpy as np
import urllib
from urllib.request import Request
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import PIL, os

class ListedCoinObject():
    def __init__(self, id, market_cap_rank, image, name, symbol, current_price, 
                 price_change_percentage_1h_in_currency, price_change_percentage_24h_in_currency, 
                 price_change_percentage_7d_in_currency, total_volume, market_cap):
        self.id = id
        self.market_cap_rank = market_cap_rank
        self.image = image
        self.name = name
        self.symbol = symbol.upper()
        self.current_price = format_currency(current_price)
        self.price_change_percentage_1h_in_currency = format_percentage(price_change_percentage_1h_in_currency)
        self.price_change_percentage_24h_in_currency = format_percentage(price_change_percentage_24h_in_currency)
        self.price_change_percentage_7d_in_currency = format_percentage(price_change_percentage_7d_in_currency)
        self.total_volume = total_volume
        self.market_cap = market_cap

class CoinDetailsObject():
    def __init__(self, id, market_cap_rank, image, name, symbol, current_price, 
                 market_cap, total_volume, circulating_supply, ath, atl, price_change_percentage_1h, 
                 price_change_percentage_24h, price_change_percentage_7d, price_change_percentage_14d,
                 price_change_percentage_30d, price_change_percentage_1y, sparkline, last_updated):
        self.id = id
        self.market_cap_rank = market_cap_rank
        self.image = image
        self.name = name
        self.symbol = symbol.upper()

        self.current_price = format_currency(current_price)
        self.market_cap = market_cap
        self.total_volume = total_volume
        self.circulating_supply = circulating_supply
        self.ath = format_currency(ath)
        self.atl = format_currency(atl)
        
        self.price_change_percentage_1h = format_percentage(price_change_percentage_1h)
        self.price_change_percentage_24h  = format_percentage(price_change_percentage_24h)
        self.price_change_percentage_7d = format_percentage(price_change_percentage_7d)
        self.price_change_percentage_14d = format_percentage(price_change_percentage_14d)
        self.price_change_percentage_30d = format_percentage(price_change_percentage_30d)
        self.price_change_percentage_1y = format_percentage(price_change_percentage_1y)
        self.sparkline = sparkline
        self.last_updated = datetime.datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")
        

#   return (int(global_data['total_market_cap']['usd']), int(global_data['total_volume']['usd']), 
#                     global_data['market_cap_percentage']['btc'], global_data['active_cryptocurrencies'], global_data['market_cap_change_percentage_24h_usd'])

class GlobalCoinDataObject():
     def __init__(self, total_market_cap, total_volume, btc_dominance, active_cryptocurrencies, market_cap_change_percentage_24h):
         self.total_market_cap = total_market_cap
         self.total_volume = total_volume
         self.btc_dominance = btc_dominance
         self.active_cryptocurrencies = active_cryptocurrencies
         self.market_cap_change_percentage_24h = market_cap_change_percentage_24h
    
class CoinLogoWidget(QLabel):
        def __init__(self, coin_id, imagePath, parent, size):
            super(QLabel, self).__init__()
            pixmap = download_and_cache_coin_image(coin_id, imagePath, parent.view.ratio, size)
            self.setPixmap(pixmap)

def download_and_cache_coin_image(coin_id, imagePath, ratio, size):
    try:
        if not os.path.exists(f'./cache/{coin_id}_{int(ratio * size)}.png'):
            url = imagePath
            request_site = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(request_site)
            image = PIL.Image.open(data)
            smaller_image = image.resize((int(size * ratio), int(size * ratio)), PIL.Image.ANTIALIAS)
            smaller_image.save(f'./cache/{coin_id}_{int(ratio * size)}.png')
        return QtGui.QPixmap(f'./cache/{coin_id}_{int(ratio * size)}.png')
    except Exception as e:
        print(e)
        return QtGui.QPixmap(f'./cache/bitcoin_{int(ratio * size)}.png')

def format_currency(currency, precission = 3):
    try:
        # sci_currency = "{:.3e}".format(currency)
        sci_currency = f"{{:.{precission}e}}".format(currency)
        number = decimal.Decimal(sci_currency)
        return number
    except Exception as e:
        # print(e)
        return 0.0
        
def format_percentage(percent):
    try:
        return round(percent, 1)
    except Exception as e:
        # print(e)
        return '—'
    
    
    
               
          