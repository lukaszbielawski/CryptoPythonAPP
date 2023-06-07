import string, decimal, datetime, math
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
        self.current_price = current_price
        self.price_change_percentage_1h_in_currency = price_change_percentage_1h_in_currency
        self.price_change_percentage_24h_in_currency = price_change_percentage_24h_in_currency
        self.price_change_percentage_7d_in_currency = price_change_percentage_7d_in_currency
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

        self.current_price = current_price
        self.market_cap = market_cap
        self.total_volume = total_volume
        self.circulating_supply = circulating_supply
        self.ath = ath
        self.atl = atl
        
        self.price_change_percentage_1h = price_change_percentage_1h
        self.price_change_percentage_24h  = price_change_percentage_24h
        self.price_change_percentage_7d = price_change_percentage_7d
        self.price_change_percentage_14d = price_change_percentage_14d
        self.price_change_percentage_30d = price_change_percentage_30d
        self.price_change_percentage_1y = price_change_percentage_1y
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
        
def format_percentage(percent):
    try:
        return f'{round(percent, 1)}%'
    except Exception as e:
        return '—'
    
def format_price(price):
    if price >= 1.0:
        return '${:,.2f}'.format(price)
    elif price <= -1.0:
        return '-${:,.2f}'.format(abs(price))
    elif price > 0.0:
        zeros = abs(math.ceil(math.log10(price)))
        return f'${{:.{zeros + 4}f}}'.format(price)
    elif price < 0.0:
        zeros = abs(math.ceil(math.log10(abs(price))))
        return f'-${{:.{zeros + 4}f}}'.format(abs(price))
    else:
        return '$0.00'

def format_big_price(price):
    return '${:,}'.format(int(price))

def format_number(number):
    return '{:,}'.format(number)

def convert_number_to_written(number):
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

if __name__ == '__main__':
    pass
    # format_price(26810.51017546782)# == 26810.51
    # format_price(0.00000734921408550618) #== 0.000007349
    # format_price(0.088613213534) #== 0.08861


               
          