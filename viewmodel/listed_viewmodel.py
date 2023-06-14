from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QTableWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from view.view import View
from model.APIFetcher import APIFetcher
import model.coins_utils as utils
from resources.Constants import Color
from abc import ABC

class ListedViewModel(ABC):
    #Abstract class which contains many common fields and methods of favourites, portfolio and master view models 
    def __init__(self, view: View, main_vm, api: APIFetcher, table_widget: QTableWidget):
        self.view = view
        self.main_vm = main_vm
        self.api = api
        self.row_count = 0
        self.table_widget = table_widget
        self._initFont()
        self.table_widget.cellClicked.connect(self.getClickedRow)


    def _initFont(self):
        #Creates and stores font
        self.arial = QFont()
        self.arial.setFamily('Arial')
        self.arial.setPixelSize(int(20 * self.view.ratio))
        

    def addRow(self, index, coin_id, no, coin_logo, coin_name, coin_symbol, price, one_hour, twenty_four_hour, seven_days, volume, market_cap):
        #This method configures and addes row to proper table_widget 
        self.row_count += 1
        self.table_widget.setRowCount(self.row_count)
        self.table_widget.setRowHeight(index, int(28 * self.view.ratio))

        coin_data_widget = QWidget()

        coin_data_layout = QHBoxLayout()
        coin_data_layout.setContentsMargins(8,0,0,0)
        coin_data_layout.setSpacing(int(8 * self.view.ratio))

        coin_logo_widget = utils.CoinLogoWidget(coin_id, coin_logo, self, 20)
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
        self.addItemAt(index, 2, QLabel(utils.format_price(price)))
        self.addItemAt(index, 3, QLabel(utils.format_percentage(one_hour)), value=one_hour)
        self.addItemAt(index, 4, QLabel(utils.format_percentage(twenty_four_hour)), value=twenty_four_hour)
        self.addItemAt(index, 5, QLabel(utils.format_percentage(seven_days)), value=seven_days)
        self.addItemAt(index, 6, QLabel(utils.format_big_price(volume)))
        self.addItemAt(index, 7, QLabel(utils.format_big_price(market_cap)))
   

    def addItemAt(self, row, column, item: QWidget, layout=None, value=None):
        #Add proper widgets to proper cells in row and customize these cells
        if column in (3, 4, 5):
            if value == None:
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
                coin_name_widget.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + 
                "; color : " + Color.WHITE.value + ";}")
                coin_symbol_widget.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + 
                "; font-size: " + str(int(16 * self.view.ratio)) + "px; color : " + Color.DARK_GRAY.value + ";}")
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
