from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import view.view as view
import viewmodel.details_viewmodel as details_vm
from model.APIFetcher import APIFetcher
from model.ListedCoinObject import ListedCoinObject
import urllib, threading, io, os
import urllib.request
from urllib.request import Request
import PIL, math
from resources.Constants import Color

class MasterViewModel():
    def __init__(self, view: view.View, main_vm, api: APIFetcher):
        print('master init')
        self.view = view
        self.main_vm = main_vm
        self.api = api
        self.row_count = 0
        self.readyToScroll = True
        self.already_loaded = 0
        self.per_page = 40
        self.setMarketCapSuffixLabel(1.21, -7.0)
        self.setMarketCapWidgetValue('$931,333,754,362')
        self.setTradingVolumeWidgetValue('$31,333,754,362')
        self.setBtcDominanceWidgetValue('43.5%')
        self.setNumberOfCoinsValue(500)
        self.__initFont()
        self.__cfgTable()
        self.loadGlobalStats()
        self.loadPage()
        # self.loadPage(100)
    
    class CoinLogoWidget(QLabel):
        def __init__(self, coin_id, imagePath, parent):
            super(QLabel, self).__init__()
            
            try:
                # raise Exception()
                if not os.path.exists(f'./cache/{coin_id}.png'):
                    url = imagePath
                    request_site = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    data = urllib.request.urlopen(request_site)
                    # urllib.request.urlretrieve(request_site, ')
                    image = PIL.Image.open(data)
                    smaller_image = image.resize((int(20 * parent.view.ratio), int(20 * parent.view.ratio)), PIL.Image.ANTIALIAS)
                    smaller_image.save(f'./cache/{coin_id}_{parent.view.ratio}.png' )
                pixmap = QtGui.QPixmap(f'./cache/{coin_id}_{parent.view.ratio}.png')
            except Exception as e:
                print(e)
                pixmap = QtGui.QPixmap(f'./cache/bitcoin_{parent.view.ratio}.png')
            # smaller_pic = pixmap.scaled(int(20 * parent.view.ratio), int(20 * parent.view.ratio))
            self.setPixmap(pixmap)

    def __initFont(self):
        self.arial = QFont()
        self.arial.setFamily('Arial')
        self.arial.setPixelSize(int(20 * self.view.ratio))
        

    def addRow(self, index, coin_id, no, coin_logo, coin_name, coin_symbol, price, one_hour, twenty_four_hour, seven_days, volume, market_cap):
        
        self.row_count += 1
        self.view.master_table_widget.setRowCount(self.row_count)
        self.view.master_table_widget.setRowHeight(index, int(28 * self.view.ratio))

        coin_data_widget = QWidget()

        coin_data_layout = QHBoxLayout()
        coin_data_layout.setContentsMargins(8,0,0,0)
        coin_data_layout.setSpacing(int(8 * self.view.ratio))

        coin_logo_widget = self.CoinLogoWidget(coin_id, coin_logo, self)
        coin_name_widget = QLabel(str(coin_name))
        coin_symbol_widget = QLabel(str(coin_symbol))

        coin_data_layout.addWidget(coin_logo_widget)
        coin_data_layout.addWidget(coin_name_widget)
        coin_data_layout.addWidget(coin_symbol_widget)
        coin_data_layout.addSpacerItem(QSpacerItem(int(10 * self.view.ratio), int(20 * self.view.ratio), QSizePolicy.Minimum, QSizePolicy.Expanding))
        coin_data_layout.setStretch(0, 0)
        coin_data_layout.setStretch(1, 0)
        coin_data_layout.setStretch(2, 0)
        coin_data_layout.setStretch(3, 1)

        coin_data_widget.setLayout(coin_data_layout)
        ##miejsca znaczae




        self.addItemAt(index, 0, QLabel(str(no))) #git
        self.addItemAt(index, 1, coin_data_widget, layout=coin_data_layout) 

        self.addItemAt(index, 2, QLabel('${:,f}'.format(price)))
        self.addItemAt(index, 3, QLabel(str(one_hour) +'%'), value=one_hour)
        self.addItemAt(index, 4, QLabel(str(twenty_four_hour)+'%'), value=twenty_four_hour)
        self.addItemAt(index, 5, QLabel(str(seven_days)+'%'), value=seven_days)
        self.addItemAt(index, 6, QLabel('${:,}'.format(volume)))
        self.addItemAt(index, 7, QLabel('${:,}'.format(market_cap)))


    def __cfgTable(self):
        self.view.master_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.master_table_widget.setFocusPolicy(Qt.NoFocus)
        self.view.master_table_widget.setSelectionMode(QAbstractItemView.NoSelection)       
       
        self.view.master_table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.master_table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.master_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.view.master_table_widget.verticalHeader().setMaximumSectionSize(int(36 * self.view.ratio))
        self.view.master_table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.view.master_table_widget.setColumnWidth(0, int(91 * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(1, int(573 * self.view.ratio)) #637
        self.view.master_table_widget.setColumnWidth(2, int(282 * self.view.ratio))#218
        self.view.master_table_widget.setColumnWidth(3, int(127 * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(4, int(127 * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(5, int(127 * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(6, int(255 * self.view.ratio))

        self.view.master_table_widget.cellClicked.connect(self.getClickedRow)

        self.view.master_table_widget.verticalScrollBar().valueChanged.connect(self.onMasterTableScroll)
        # self.view.master_table_widget.setColumnWidth(7, int(350 * self.view.ratio))

    def addItemAt(self, row, column, item: QWidget, layout=None, value=None):
        # item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
      
        
        if column in (3, 4, 5):
            if type(value) == str:
                color = Color.WHITE.value
            else:
                color = Color.GREEN.value if value >= 0.0 else Color.RED.value

        match column:
            case 0:
                color = Color.WHITE.value
                
            case 1:
                coin_name_widget = layout.itemAt(1).widget()
                coin_name_widget.setFont(self.arial)
                coin_symbol_widget = layout.itemAt(2).widget()
                coin_symbol_widget.setFont(self.arial)
                coin_name_widget.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : " + Color.WHITE.value + ";}")
                coin_symbol_widget.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); font-size: " + str(int(16 * self.view.ratio)) + "px; color : " + Color.DARK_GRAY.value + ";}")
            case 2:
                color = Color.WHITE.value
            case 6:
                color = Color.BLUE_GRAY.value
            case 7:
                color = Color.BLUE_GRAY.value
            case _:
                pass
        if column != 1:
            item.setAlignment(Qt.AlignCenter)
            
                # item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : " + Color.DARK_GRAY.value + ";}")
            item.setFont(self.arial)
                # item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : " + Color.BLUE_GRAY.value + ";}")
            item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : " + color + ";}")
        self.view.master_table_widget.setCellWidget(row, column, item)   

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
        print(self.already_loaded + self.per_page > self.api.coins_loaded)
        if self.already_loaded + self.per_page > self.api.coins_loaded:
            self.api.fetchNewListedCoins()
        try:
            coins = self.api.listed_coins_array
            for i in range(self.per_page):
                # self.addRow(i + offset, int(self.row_count + 1), './resources/logo.png', 'Bitcoin', 'BTC', '$26,961.43', '-0.1%', '-2.6%', '+2.4%', '$16,332,763,917', '$522,840,485,971')
                self.addRow(self.already_loaded + i, coins[self.already_loaded + i].id, coins[self.already_loaded + i].market_cap_rank, coins[self.already_loaded + i].image, coins[self.already_loaded + i].name, 
                        coins[self.already_loaded + i].symbol, coins[self.already_loaded + i].current_price, coins[self.already_loaded + i].price_change_percentage_1h_in_currency,
                          coins[self.already_loaded + i].price_change_percentage_24h_in_currency, coins[self.already_loaded + i].price_change_percentage_7d_in_currency, 
                          coins[self.already_loaded + i].total_volume, coins[self.already_loaded + i].market_cap)
            self.already_loaded += self.per_page
        except Exception as e:
            print(e)


    # return (global_data['total_market_cap']['usd'], global_data['total_volume']['usd'], 
    #                 global_data['market_cap_percentage']['btc'], global_data['active_cryptocurrencies'], global_data['market_cap_change_percentage_24h_usd'])

    def loadGlobalStats(self):
        tuple = self.api.global_data_tuple
        self.setMarketCapSuffixLabel(tuple[0], tuple[4])
        self.setMarketCapWidgetValue('${:,}'.format(tuple[0]))
        self.setTradingVolumeWidgetValue('${:,}'.format(tuple[1]))
        self.setBtcDominanceWidgetValue(str(self.__format_percentage(tuple[2])) + '%')
        self.setNumberOfCoinsValue('{:,}'.format(tuple[3]))


    def __format_percentage(self, percent):
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
            self.view.market_cap_suffix_label.setText(f'{self.__convert_number_to_written(value)}, a <font color=#54EE1F>{self.__format_percentage(change)}%</font> increase in the last 24 hours.')
        else:
            self.view.market_cap_suffix_label.setText(f'{self.__convert_number_to_written(value)}, a <font color=#F0302C>{self.__format_percentage(change)}%</font> decrease in the last 24 hours.')
    
    def setMarketCapWidgetValue(self, value):
        self.view.market_cap_widget_value.setText(str(value))

    def setTradingVolumeWidgetValue(self, value):
        self.view.trading_volume_widget_value.setText(str(value))

    def setBtcDominanceWidgetValue(self, value):
        self.view.btc_dominance_widget_value.setText(str(value))

    def setNumberOfCoinsValue(self, value):
        self.view.number_of_coins_widget_value.setText(str(value))

    def getClickedRow(self, row, column):
        self.main_vm.detailsRequest()
        print(row) 


