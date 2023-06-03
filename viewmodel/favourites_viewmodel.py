from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
from view.view import View
from viewmodel.details_viewmodel import DetailsViewModel
from model.APIFetcher import APIFetcher

class FavouritesViewModel():
    def __init__(self, view: View, main_vm, api: APIFetcher):
        print('fav init')
        self.view = view
        self.main_vm = main_vm
        self.number_of_coins = 0
        self.__cfgTable()
        self.view.favourites_table.setRowCount(self.number_of_coins)
        self.addRow('1', './resources/logo.png', 'Bitcoin', 'BTC', '$26,961.43', '-0.1%', '-2.6%', '+2.4%', '$16,332,763,917', '$522,840,485,971')
        self.addRow('2', './resources/logo.png', 'Bitcoin', 'BTC', '$26,961.43', '-0.1%', '-2.6%', '+2.4%', '$16,332,763,917', '$522,840,485,971')

        self.setNumberOfFavouriteCoinsValue()
        
    class CoinLogoWidget(QLabel):
        def __init__(self, imagePath, parent):
            super(QLabel, self).__init__()
            pixmap = QtGui.QPixmap(imagePath)
            smaller_pic = pixmap.scaled(int(20 * parent.view.ratio), int(20 * parent.view.ratio))
            self.setPixmap(smaller_pic)

    def addRow(self, no, coin_logo, coin_name, coin_symbol, price, one_hour, twenty_four_hour, seven_days, volume, market_cap):
        
        self.number_of_coins += 1
        self.view.favourites_table.setRowCount(self.number_of_coins)
        self.view.favourites_table.setRowHeight(self.number_of_coins - 1, int(28 * self.view.ratio))

        coin_data_widget = QWidget()

        coin_data_layout = QHBoxLayout()
        coin_data_layout.setContentsMargins(8,0,0,0)
        coin_data_layout.setSpacing(int(8 * self.view.ratio))

        coin_logo_widget = self.CoinLogoWidget(coin_logo, self)
        coin_name_widget = QLabel(coin_name)
        coin_symbol_widget = QLabel(coin_symbol)

        coin_data_layout.addWidget(coin_logo_widget)
        coin_data_layout.addWidget(coin_name_widget)
        coin_data_layout.addWidget(coin_symbol_widget)
        coin_data_layout.addSpacerItem(QSpacerItem(int(10 * self.view.ratio), int(20 * self.view.ratio), QSizePolicy.Minimum, QSizePolicy.Expanding))
        coin_data_layout.setStretch(0, 0)
        coin_data_layout.setStretch(1, 0)
        coin_data_layout.setStretch(2, 0)
        coin_data_layout.setStretch(3, 1)

        coin_data_widget.setLayout(coin_data_layout)

        self.addItemAt(self.number_of_coins -1, 0, QLabel(no))
        self.addItemAt(self.number_of_coins -1, 1, coin_data_widget, coin_data_layout)
        self.addItemAt(self.number_of_coins -1, 2, QLabel(price))
        self.addItemAt(self.number_of_coins -1, 3, QLabel(one_hour))
        self.addItemAt(self.number_of_coins -1, 4, QLabel(twenty_four_hour))
        self.addItemAt(self.number_of_coins -1, 5, QLabel(seven_days))
        self.addItemAt(self.number_of_coins -1, 6, QLabel(volume))
        self.addItemAt(self.number_of_coins -1, 7, QLabel(market_cap))


        

    def __cfgTable(self):
        self.view.favourites_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.favourites_table.setFocusPolicy(Qt.NoFocus)
        self.view.favourites_table.setSelectionMode(QAbstractItemView.NoSelection)       
        self.view.favourites_table.cellClicked.connect(self.getClickedRow)
        self.view.favourites_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.favourites_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.favourites_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.view.favourites_table.verticalHeader().setMaximumSectionSize(int(36 * self.view.ratio))
        self.view.favourites_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.view.favourites_table.setColumnWidth(0, int(91 * self.view.ratio))
        self.view.favourites_table.setColumnWidth(1, int(637 * self.view.ratio))
        self.view.favourites_table.setColumnWidth(2, int(218 * self.view.ratio))
        self.view.favourites_table.setColumnWidth(3, int(127 * self.view.ratio))
        self.view.favourites_table.setColumnWidth(4, int(127 * self.view.ratio))
        self.view.favourites_table.setColumnWidth(5, int(127 * self.view.ratio))
        self.view.favourites_table.setColumnWidth(6, int(255 * self.view.ratio))
        # self.view.favourites_table.setColumnWidth(7, int(350 * self.view.ratio))

    def addItemAt(self, row, column, item: QWidget, layout=None):
        # item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
        
        arial = QFont()
        arial.setFamily('Arial')
        
        if column != 1:
            item.setAlignment(Qt.AlignCenter)
            item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #778899;}")

        match column:
            case 0:
                item.setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 0); color: white;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 1:
                arial.setPixelSize(int(20 * self.view.ratio))
                coin_name_widget = layout.itemAt(1).widget()
                coin_name_widget.setFont(arial)
                coin_symbol_widget = layout.itemAt(2).widget()
                coin_symbol_widget.setFont(arial)
                coin_name_widget.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
                coin_symbol_widget.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); font-size: " + str(int(16 * self.view.ratio)) + "px; color : #778899;}")
            case 2:
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
                item.setFont(arial)
            case 3:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #F0302C;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 4:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #F0302C;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 5:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #54EE1F;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 6:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #CBD0DE;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case _:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #CBD0DE;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
        
        self.view.favourites_table.setCellWidget(row, column, item)   

    def setNumberOfFavouriteCoinsValue(self):
        self.view.favourites_number_of_favourite_coins_value.setText(str(self.number_of_coins))

    def getClickedRow(self, row, column):
        self.main_vm.detailsRequest()
        print(row)


