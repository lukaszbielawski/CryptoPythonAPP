import datetime, math, urllib, PIL, os
from urllib.request import Request
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel

class ListedCoinObject():
    #A class that stores primary data about a coin
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
    #A class that stores detailed data about a coin
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

class GlobalCoinDataObject():
    #A class that stores global data about whole cryptocurrency market
     def __init__(self, total_market_cap, total_volume, btc_dominance, active_cryptocurrencies, market_cap_change_percentage_24h):
         self.total_market_cap = total_market_cap
         self.total_volume = total_volume
         self.btc_dominance = btc_dominance
         self.active_cryptocurrencies = active_cryptocurrencies
         self.market_cap_change_percentage_24h = market_cap_change_percentage_24h
    
class CoinLogoWidget(QLabel):
    #Custom class that displays image in label
        def __init__(self, coin_id, imagePath, parent, size):
            super(QLabel, self).__init__()
            pixmap = download_and_cache_coin_image(coin_id, imagePath, parent.view.ratio, size)
            self.setPixmap(pixmap)

def download_and_cache_coin_image(coin_id, imagePath, ratio, size):
    #This function is checking for existence of proper image in cache and if it is not found then it downloads it
    #After download this function resizes image and store it in cache.
    #Regardles of initial appearance of image in cache it returns QPixMap which contains fetched image

    try:
        if not os.path.exists(f'./cache/{coin_id}_{int(ratio * size)}.png'):
            if not os.path.exists('./cache'): os.mkdir('./cache', mode = 0o777)
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
    #This function formats percentage values to display it in proper form
    try:
        return f'{round(percent, 1)}%'
    except Exception as e:
        return '—'
    
def format_price(price):
    #This function formats prices to display it in proper form
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
    #This function formats big prices to display it in proper form
    return '${:,}'.format(int(price))

def format_number(number):
    #This function formats numbers which are not prices to display it in proper form
    return '{:,}'.format(number)

def convert_number_to_written(number):
    #This function convert numeric number to written number ex. 1 213 531 213 to Bilion
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

               
          