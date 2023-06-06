from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QTableWidget
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
from view.view import View
import viewmodel.details_viewmodel as details_vm
from model.APIFetcher import APIFetcher
from model.coins_utils import ListedCoinObject, CoinLogoWidget
import urllib, threading, io, os
import urllib.request
from urllib.request import Request
import PIL, math
from resources.Constants import Color, ViewModel
from abc import ABC, abstractmethod

class ListedViewModel(ABC):
    def __init__(self, view: View, main_vm, api: APIFetcher, table_widget: QTableWidget):
        self.view = view
        self.main_vm = main_vm
        self.api = api
        self.row_count = 0
        self.table_widget = table_widget
        self._initFont()
        self._cfgTable()


    def _initFont(self):
        self.arial = QFont()
        self.arial.setFamily('Arial')
        self.arial.setPixelSize(int(20 * self.view.ratio))
        

    def addRow(self, index, coin_id, no, coin_logo, coin_name, coin_symbol, price, one_hour, twenty_four_hour, seven_days, volume, market_cap):
        
        self.row_count += 1
        self.table_widget.setRowCount(self.row_count)
        self.table_widget.setRowHeight(index, int(28 * self.view.ratio))

        coin_data_widget = QWidget()

        coin_data_layout = QHBoxLayout()
        coin_data_layout.setContentsMargins(8,0,0,0)
        coin_data_layout.setSpacing(int(8 * self.view.ratio))

        coin_logo_widget = CoinLogoWidget(coin_id, coin_logo, self, 20)
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


        self.addItemAt(index, 0, QLabel(str(no)))
        self.addItemAt(index, 1, coin_data_widget, layout=coin_data_layout) 
        self.addItemAt(index, 2, QLabel('${:,f}'.format(price)))
        self.addItemAt(index, 3, QLabel(str(one_hour) +'%'), value=one_hour)
        self.addItemAt(index, 4, QLabel(str(twenty_four_hour)+'%'), value=twenty_four_hour)
        self.addItemAt(index, 5, QLabel(str(seven_days)+'%'), value=seven_days)
        self.addItemAt(index, 6, QLabel('${:,}'.format(volume)))
        self.addItemAt(index, 7, QLabel('${:,}'.format(market_cap)))

    
    def _cfgTable(self):
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setFocusPolicy(Qt.NoFocus)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)       
       
        self.table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_widget.verticalHeader().setMaximumSectionSize(int(36 * self.view.ratio))
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.table_widget.setColumnWidth(0, int(91 * self.view.ratio))
        self.table_widget.setColumnWidth(1, int(573 * self.view.ratio)) #637
        self.table_widget.setColumnWidth(2, int(282 * self.view.ratio))#218
        self.table_widget.setColumnWidth(3, int(127 * self.view.ratio))
        self.table_widget.setColumnWidth(4, int(127 * self.view.ratio))
        self.table_widget.setColumnWidth(5, int(127 * self.view.ratio))
        self.table_widget.setColumnWidth(6, int(255 * self.view.ratio))

        self.table_widget.cellClicked.connect(self.getClickedRow)

    def addItemAt(self, row, column, item: QWidget, layout=None, value=None):

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
                coin_name_widget.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; color : " + Color.WHITE.value + ";}")
                coin_symbol_widget.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; font-size: " + str(int(16 * self.view.ratio)) + "px; color : " + Color.DARK_GRAY.value + ";}")
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
            item.setFont(self.arial)
            item.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; color : " + color + ";}")
        self.table_widget.setCellWidget(row, column, item)

        @abstractmethod 
        def getClickedRow(self, row, column):
            pass

