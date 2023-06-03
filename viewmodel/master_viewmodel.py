from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import view.view as view
import viewmodel.details_viewmodel as details_vm
from model.APIFetcher import APIFetcher
from model.ListedCoinObject import ListedCoinObject
import time
import urllib
from urllib.request import Request, urlopen

class MasterViewModel():
    def __init__(self, view: view.View, main_vm, api: APIFetcher):
        print('master init')
        self.view = view
        self.main_vm = main_vm
        self.api = api
        self.row_count = 0
        self.readyToScroll = True
        self.setMarketCapSuffixLabel(1.21, -7.0)
        self.setMarketCapWidgetValue('$931,333,754,362')
        self.setTradingVolumeWidgetValue('$31,333,754,362')
        self.setBtcDominanceWidgetValue('43.5%')
        self.setNumberOfCoinsValue(500)
        self.__initFont()
        self.__cfgTable()
        

        self.loads = 0
        
        self.loadPage()
        # self.loadPage(100)

    class CoinLogoWidget(QLabel):
        def __init__(self, imagePath, parent):
            super(QLabel, self).__init__()
            url = imagePath
            request_site = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(request_site).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            smaller_pic = pixmap.scaled(int(20 * parent.view.ratio), int(20 * parent.view.ratio))
            self.setPixmap(smaller_pic)
    
    def __initFont(self):
        self.arial = QFont()
        self.arial.setFamily('Arial')
        self.arial.setPixelSize(int(20 * self.view.ratio))
        

    def addRow(self, index, no, coin_logo, coin_name, coin_symbol, price, one_hour, twenty_four_hour, seven_days, volume, market_cap):
        
        self.row_count += 1
        self.view.master_table_widget.setRowCount(self.row_count)
        self.view.master_table_widget.setRowHeight(index, int(28 * self.view.ratio))

        coin_data_widget = QWidget()

        coin_data_layout = QHBoxLayout()
        coin_data_layout.setContentsMargins(8,0,0,0)
        coin_data_layout.setSpacing(int(8 * self.view.ratio))

        coin_logo_widget = self.CoinLogoWidget(str(coin_logo), self)
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
        self.addItemAt(index, 0, QLabel(str(no)))
        self.addItemAt(index, 1, coin_data_widget, coin_data_layout)
        self.addItemAt(index, 2, QLabel(str(price)))
        self.addItemAt(index, 3, QLabel(str(one_hour)))
        self.addItemAt(index, 4, QLabel(str(twenty_four_hour)))
        self.addItemAt(index, 5, QLabel(str(seven_days)))
        self.addItemAt(index, 6, QLabel(str(volume)))
        self.addItemAt(index, 7, QLabel(str(market_cap)))


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
        self.view.master_table_widget.setColumnWidth(1, int(637 * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(2, int(218 * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(3, int(127 * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(4, int(127 * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(5, int(127 * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(6, int(255 * self.view.ratio))

        self.view.master_table_widget.cellClicked.connect(self.getClickedRow)

        self.view.master_table_widget.verticalScrollBar().valueChanged.connect(self.onMasterTableScroll)
        # self.view.master_table_widget.setColumnWidth(7, int(350 * self.view.ratio))

    def addItemAt(self, row, column, item: QWidget, layout=None):
        # item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
        
        
        if column != 1:
            item.setAlignment(Qt.AlignCenter)
            item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #778899;}")
            item.setFont(self.arial)

        match column:
            case 0:
                item.setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 0); color: white;}")
            case 1:
                coin_name_widget = layout.itemAt(1).widget()
                coin_name_widget.setFont(self.arial)
                coin_symbol_widget = layout.itemAt(2).widget()
                coin_symbol_widget.setFont(self.arial)
                coin_name_widget.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
                coin_symbol_widget.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); font-size: " + str(int(16 * self.view.ratio)) + "px; color : #778899;}")
            case 2:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
            case 3:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #F0302C;}")
            case 4:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #F0302C;}")
            case 5:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #54EE1F;}")
            case 6:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #CBD0DE;}")
            case _:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #CBD0DE;}")
        
        self.view.master_table_widget.setCellWidget(row, column, item)   

    def onMasterTableScroll(self, *args):
        rect = self.view.master_table_widget.viewport().rect()
        top_index = self.view.master_table_widget.indexAt(rect.topLeft()).row()
        print(top_index)
        if top_index >= (250 * self.loads - 50) and self.readyToScroll:
            self.readyToScroll = False
            self.loadPage(250 * self.loads)
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
        

    def loadPage(self, offset=0):
        self.loads += 1
        print(offset)
        coins: list[ListedCoinObject] = self.api.fetchNewListedCoins(offset // 250)
        if coins != None:
            print(len(coins))
            for i in range(250):
                # self.addRow(i + offset, int(self.row_count + 1), './resources/logo.png', 'Bitcoin', 'BTC', '$26,961.43', '-0.1%', '-2.6%', '+2.4%', '$16,332,763,917', '$522,840,485,971')
                self.addRow(i + offset, coins[i + offset].market_cap_rank, coins[i + offset].image, coins[i + offset].name, 
                        coins[i + offset].symbol, coins[i + offset].current_price, coins[i + offset].price_change_percentage_1h_in_currency,
                          coins[i + offset].price_change_percentage_24h_in_currency, coins[i + offset].price_change_percentage_7d_in_currency, 
                          coins[i + offset].total_volume, coins[i + offset].market_cap)
        else:
            print('Cannot load data')

    def setMarketCapSuffixLabel(self, value, change):
        if change >= 0:
            self.view.market_cap_suffix_label.setText(f'{value} Trillion, a <font color=#54EE1F{change}%</font> increase in the last 24 hours.')
        else:
            self.view.market_cap_suffix_label.setText(f'{value} Trillion, a <font color=#F0302C>{change}%</font> decrease in the last 24 hours.')
    
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


